from django import forms
from django.utils.translation import ugettext_lazy as _


class ImportForm(forms.Form):

    file = forms.FileField(label=_('Xls-file'))
