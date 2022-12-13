from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .forms import MessageForm
from .tasks import send_message_all


class MessageView(FormView):
    """
    Вьюха для рассыки сообщений в админке
    """

    template_name = 'profi/message.html'
    form_class = MessageForm
    success_url = reverse_lazy('profi:message')

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(MessageView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _('The message was successfully sent out'))
        send_message_all.delay(form.cleaned_data['message'])
        return super(MessageView, self).form_valid(form)
