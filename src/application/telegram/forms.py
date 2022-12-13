import os

from django import forms
from django.utils.translation import ugettext_lazy as _


class MessageForm(forms.Form):
    """
    Форма рассылки сообщений для админки
    """
    message = forms.CharField(label=_('Message text'), widget=forms.Textarea(attrs={'class': 'vLargeTextField'}))


class MessageGroupForm(forms.Form):
    excel_file = forms.FileField(label=_('Excel file'))

    def clean_excel_file(self):
        data = self.cleaned_data['excel_file']

        filename, file_extension = os.path.splitext(str(data))
        if file_extension != '.xlsx':
            raise forms.ValidationError(_('This file is not Excel document. You need upload file with .xlsx extension.'))

        return data


class MessageGroupFileForm(forms.Form):

    file = forms.FileField(label=_('File'), required=False)
    message = forms.CharField(label=_('Message text'), widget=forms.Textarea(attrs={'class': 'vLargeTextField'}))


class MessageStoresFileForm(forms.Form):

    file = forms.FileField(label=_('File'), required=False)
    message = forms.CharField(label=_('Message text'), widget=forms.Textarea(attrs={'class': 'vLargeTextField'}))
    is_order_button = forms.BooleanField(label=_('Order button'), required=False)
