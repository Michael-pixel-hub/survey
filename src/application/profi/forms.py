from django import forms
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

from .models import Order


class MessageForm(forms.Form):
    """
    Форма рассылки сообщений для админки
    """
    message = forms.CharField(label=_('Message text'), widget=forms.Textarea(attrs={'class': 'vLargeTextField'}))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('__all__')
        widgets = {
            'clients': autocomplete.ModelSelect2Multiple(
                url='survey:ac-clients',
                attrs={
                    'data-placeholder': _('One or any clients'),
                    #'data-minimum-input-length': 3,
                },
            ),
            'stores': autocomplete.ModelSelect2Multiple(
                url='survey:ac-stores',
                attrs={
                    'data-placeholder': _('One or any stores'),
                    # 'data-minimum-input-length': 3,
                },
            ),
            'regions': autocomplete.ModelSelect2Multiple(
                url='survey:ac-regions',
                attrs={
                    'data-placeholder': _('One or any regions'),
                    # 'data-minimum-input-length': 3,
                },
            )
        }
