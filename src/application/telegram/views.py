import os
import tempfile

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .forms import MessageForm, MessageGroupForm, MessageGroupFileForm, MessageStoresFileForm
from .tasks import send_message_all

from application.survey.utils import get_send_message_data, get_send_message_data_stores


class MessageView(FormView):
    """
    Вьюха для рассыки сообщений в админке
    """

    template_name = 'telegram/message.html'
    form_class = MessageForm
    success_url = reverse_lazy('telegram:message')

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(MessageView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _('The message was successfully sent out'))
        send_message_all.delay(form.cleaned_data['message'])
        return super(MessageView, self).form_valid(form)


class MessageGroupView(FormView):

    template_name = 'telegram/message_group.html'
    form_class = MessageGroupForm
    temp_file = None
    temp_file_name = ''

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageGroupView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(MessageGroupView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        f = form.cleaned_data['excel_file']
        fp = tempfile.NamedTemporaryFile(dir=settings.UPLOAD_PATH, delete=False)
        fp.write(f.read())
        fp.close()
        os.rename(fp.name, fp.name + '.xlsx')
        self.temp_file = os.path.basename(fp.name + '.xlsx')
        self.temp_file_name = str(f)
        return super(MessageGroupView, self).form_valid(form)

    def get_success_url(self):
        if self.temp_file:
            return '%s?file=%s&name=%s' % (
                reverse_lazy('telegram:message_group_file'), self.temp_file, self.temp_file_name)
        else:
            return reverse_lazy('telegram:message_group')


class MessageGroupFileView(FormView):

    template_name = 'telegram/message_group_file.html'
    form_class = MessageGroupFileForm
    success_url = reverse_lazy('telegram:message_group')
    file = None

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.GET.get('file'):
            return redirect('telegram:message_group')
        self.file = os.path.join(settings.UPLOAD_PATH, self.request.GET.get('file'))
        return super(MessageGroupFileView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(MessageGroupFileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        # Context
        context = super(MessageGroupFileView, self).get_context_data(**kwargs)

        # Task execution report
        context['file_name'] = self.request.GET.get('name') if self.request.GET.get('name') else _('Uploaded file')
        context['excel_error'] = ''

        # Excel
        data = get_send_message_data(self.file)
        if type(data) == str:
            context['excel_error'] = data
            return context

        context['data'] = data
        count = 0
        for i in data:
            if i['obj']:
                count += 1
        context['count'] = count
        context['count_all'] = len(data)

        # Exit
        return context

    def form_valid(self, form):

        try:
            f = form.cleaned_data['file']
            filename, file_extension = os.path.splitext(str(f))
            fp = tempfile.NamedTemporaryFile(dir=settings.UPLOAD_PATH, delete=False)
            fp.write(f.read())
            fp.close()
            os.rename(fp.name, fp.name + file_extension)
            temp_file = os.path.basename(fp.name + file_extension)
            temp_file = os.path.join(settings.UPLOAD_PATH, temp_file)
        except:
            temp_file = None

        messages.success(self.request, _('The message was successfully sent out'))
        from application.telegram.tasks import send_messages_group
        send_messages_group.delay(form.cleaned_data['message'], temp_file, self.file)

        return super(MessageGroupFileView, self).form_valid(form)


class MessageStoresView(FormView):

    template_name = 'telegram/message_stores.html'
    form_class = MessageGroupForm
    temp_file = None
    temp_file_name = ''

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        f = form.cleaned_data['excel_file']
        fp = tempfile.NamedTemporaryFile(dir=settings.UPLOAD_PATH, delete=False)
        fp.write(f.read())
        fp.close()
        os.rename(fp.name, fp.name + '.xlsx')
        self.temp_file = os.path.basename(fp.name + '.xlsx')
        self.temp_file_name = str(f)
        return super().form_valid(form)

    def get_success_url(self):
        if self.temp_file:
            return '%s?file=%s&name=%s' % (
                reverse_lazy('telegram:message_stores_file'), self.temp_file, self.temp_file_name)
        else:
            return reverse_lazy('telegram:message_stores')


class MessageStoresFileView(FormView):

    template_name = 'telegram/message_stores_file.html'
    form_class = MessageStoresFileForm
    success_url = reverse_lazy('telegram:message_stores')
    file = None

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.GET.get('file'):
            return redirect('telegram:message_stores')
        self.file = os.path.join(settings.UPLOAD_PATH, self.request.GET.get('file'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        # Context
        context = super().get_context_data(**kwargs)

        # Task execution report
        context['file_name'] = self.request.GET.get('name') if self.request.GET.get('name') else _('Uploaded file')
        context['excel_error'] = ''

        # Excel
        data = get_send_message_data_stores(self.file)
        if type(data) == str:
            context['excel_error'] = data
            return context

        context['data'] = data
        count = 0
        for i in data:
            if i['obj']:
                count += 1
        context['count'] = count
        context['count_all'] = len(data)

        # Exit
        return context

    def form_valid(self, form):

        try:
            f = form.cleaned_data['file']
            filename, file_extension = os.path.splitext(str(f))
            fp = tempfile.NamedTemporaryFile(dir=settings.UPLOAD_PATH, delete=False)
            fp.write(f.read())
            fp.close()
            os.rename(fp.name, fp.name + file_extension)
            temp_file = os.path.basename(fp.name + file_extension)
            temp_file = os.path.join(settings.UPLOAD_PATH, temp_file)
        except:
            temp_file = None

        messages.success(self.request, _('The message was successfully sent out'))
        from application.telegram.tasks import send_messages_stores
        send_messages_stores.delay(form.cleaned_data['message'], temp_file, self.file, form.cleaned_data['is_order_button'])

        return super().form_valid(form)
