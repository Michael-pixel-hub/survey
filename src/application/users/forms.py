from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserChangePasswordForm(forms.Form):

    email = forms.EmailField(label=_('Введите e-mail'), required=True, initial='')
    password = forms.CharField(widget=forms.PasswordInput(), label=_('Введите новый пароль'), required=True,
                               initial='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label=_('Подтвердите новый пароль'), required=True,
                                       initial='')

    class Meta:
        model = User
