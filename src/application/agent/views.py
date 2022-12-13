from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import get_messages
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .forms import ImportForm
from .models import Import
from .tasks import import_data


class ImportView(FormView):

    template_name = 'agent/import.html'
    form_class = ImportForm
    success_url = reverse_lazy('agent:import')
    is_success = False

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('action') == 'cancel':
            cache.set('survey_agent_import_cancel', 1)
        return super(ImportView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        import hashlib
        import random

        try:
            Import.objects.get(status=1)
            return
        except Import.DoesNotExist:
            pass

        temp_file = '/tmp/%s.xls' % hashlib.sha1(str(random.random()).encode()).hexdigest()[:12]

        file_name = self.request.FILES['file'].name

        with open(temp_file, 'wb+') as destination:
            for chunk in self.request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()
            import_data.delay(temp_file, file_name)

        messages.success(self.request, _('Import data task sending successfully'))

        return super(ImportView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        # Context
        context = super(ImportView, self).get_context_data(**kwargs)

        # Search
        try:
            import_obj = Import.objects.get(status=1)
        except Import.DoesNotExist:
            import_obj = None

        # Messages
        storage = get_messages(self.request)
        for i in storage:
            self.is_success = True

        context['import_obj'] = import_obj
        context['is_success'] = self.is_success

        # Last import
        last_import = Import.objects.first()
        context['last_import'] = last_import

        # Exit
        return context
