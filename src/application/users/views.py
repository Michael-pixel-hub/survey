"""Docstring"""

import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .forms import UserChangePasswordForm
from .models import User

logger = logging.getLogger('django')


class UserChangePasswordView(FormView):

    """
    Изменение пароля заданного в поле формы "E-mail" пользователя
    """

    template_name = 'users/change_password.html'
    form_class = UserChangePasswordForm
    model = User
    success_url = reverse_lazy('users:password')
    is_success = False

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):

        if request.user.email not in settings.ADD_TASK_USERS:
            text_log = f'{request.user.username} нет доступа'
            logger.info(text_log)
            return HttpResponseForbidden('У вас нет прав')

        if self.request.method == 'POST':
            request.session['email'] = self.request.POST.get('email')
            form = UserChangePasswordForm(request.POST)
            if form.is_valid():
                try:
                    email = self.request.POST.get('email')
                    user = User.objects.get(email=email)
                    new_password = self.request.POST.get('password')
                    confirm_password = self.request.POST\
                        .get('confirm_password')
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        user.save()
                        request.session['email'] = ''
                        text_log = f'{request.user.username} ' \
                                   f'успешно изменил пароль'
                        logger.info(text_log)
                        messages.success(self.request,
                                         _(f'Пароль пользователя {email} '
                                           f'успешно изменен'))
                    else:
                        messages.error(self.request,
                                       _(f'Новый пароль пользователя {email}'
                                         f' не подтвержден повторным вводом'))
                except User.DoesNotExist:
                    request.session['email'] = ''
                    messages.error(self.request,
                                   _(f'Пользователь, имеющий e-mail {email} в '
                                     f'системе не существует.'))

        return super(UserChangePasswordView, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

     # Context
        context = super().get_context_data(**kwargs)
        try:
            email = self.request.session['email']
        except KeyError:
            email = ''
        context['change_password_form'] = UserChangePasswordForm(
            initial={'email': email})

     # Exit
        return context
