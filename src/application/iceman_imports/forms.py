from django import forms
from django.utils.translation import ugettext_lazy as _


class ImportStoresForm(forms.Form):

    file = forms.FileField(label=_('Xls-file'))


class ImportProductsForm(forms.Form):

    file = forms.FileField(label=_('Xls-file'))


class ImportTasksForm(forms.Form):

    file = forms.FileField(label=_('Xls-file'))
