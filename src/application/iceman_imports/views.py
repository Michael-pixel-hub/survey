from application.iceman.forms import ExportTasksForm, ExportStoresForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import get_messages
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .forms import ImportStoresForm, ImportProductsForm, ImportTasksForm
from .models import ImportStores, ImportProducts, ImportTasks
from .tasks import iceman_import_stores, iceman_import_products, iceman_import_tasks


class ImportStoresView(FormView):

    template_name = 'iceman/import-stores.html'
    form_class = ImportStoresForm
    success_url = reverse_lazy('iceman-imports:import-stores')
    is_success = False

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('action') == 'cancel':
            cache.set('iceman_import_stores_cancel', 1)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        import hashlib
        import random

        try:
            ImportStores.objects.get(status=1)
            return
        except ImportStores.DoesNotExist:
            pass

        temp_file = '/tmp/%s.xls' % hashlib.sha1(str(random.random()).encode()).hexdigest()[:12]

        file_name = self.request.FILES['file'].name

        with open(temp_file, 'wb+') as destination:
            for chunk in self.request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()
            iceman_import_stores.delay(temp_file, file_name, self.request.user.id)

        messages.success(self.request, _('Import data task sending successfully'))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        # Context
        context = super().get_context_data(**kwargs)

        # Search
        try:
            import_obj = ImportStores.objects.get(status=1)
        except ImportStores.DoesNotExist:
            import_obj = None

        # Messages
        storage = get_messages(self.request)
        for i in storage:
            self.is_success = True

        context['import_obj'] = import_obj
        context['is_success'] = self.is_success

        # Last import
        last_import = ImportStores.objects.first()
        context['last_import'] = last_import

        # Export
        context['export_form'] = ExportStoresForm()

        # Exit
        return context


class ImportProductsView(FormView):

    template_name = 'iceman/import-products.html'
    form_class = ImportProductsForm
    success_url = reverse_lazy('iceman-imports:import-products')
    is_success = False

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('action') == 'cancel':
            cache.set('iceman_import_products_cancel', 1)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        import hashlib
        import random

        try:
            ImportProducts.objects.get(status=1)
            return
        except ImportProducts.DoesNotExist:
            pass

        temp_file = '/tmp/%s.xls' % hashlib.sha1(str(random.random()).encode()).hexdigest()[:12]

        file_name = self.request.FILES['file'].name

        with open(temp_file, 'wb+') as destination:
            for chunk in self.request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()
            iceman_import_products.delay(temp_file, file_name, self.request.user.id)

        messages.success(self.request, _('Import data task sending successfully'))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        # Context
        context = super().get_context_data(**kwargs)

        # Search
        try:
            import_obj = ImportProducts.objects.get(status=1)
        except ImportProducts.DoesNotExist:
            import_obj = None

        # Messages
        storage = get_messages(self.request)
        for i in storage:
            self.is_success = True

        context['import_obj'] = import_obj
        context['is_success'] = self.is_success

        # Last import
        last_import = ImportProducts.objects.first()
        context['last_import'] = last_import

        # Exit
        return context


class ImportTasksView(FormView):

    template_name = 'iceman/import-tasks.html'
    form_class = ImportTasksForm
    success_url = reverse_lazy('iceman-imports:import-tasks')
    is_success = False

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('action') == 'cancel':
            cache.set('iceman_import_tasks_cancel', 1)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        import hashlib
        import random

        try:
            ImportTasks.objects.get(status=1)
            return
        except ImportTasks.DoesNotExist:
            pass

        temp_file = '/tmp/%s.xls' % hashlib.sha1(str(random.random()).encode()).hexdigest()[:12]

        file_name = self.request.FILES['file'].name

        with open(temp_file, 'wb+') as destination:
            for chunk in self.request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()
            iceman_import_tasks.delay(temp_file, file_name, self.request.user.id)

        messages.success(self.request, _('Import data task sending successfully'))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        # Context
        context = super().get_context_data(**kwargs)

        # Search
        try:
            import_obj = ImportTasks.objects.get(status=1)
        except ImportTasks.DoesNotExist:
            import_obj = None

        # Messages
        storage = get_messages(self.request)
        for i in storage:
            self.is_success = True

        context['import_obj'] = import_obj
        context['is_success'] = self.is_success

        # Last import
        last_import = ImportTasks.objects.first()
        context['last_import'] = last_import

        # Export
        context['export_form'] = ExportTasksForm()

        # Exit
        return context
