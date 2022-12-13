from application.survey.models import Task
from django import forms
from django.utils.translation import ugettext_lazy as _
from dal import autocomplete

from .models import Region, Source, Store
from application.survey.models import User, UserStatusIceman


class MessageForm(forms.Form):
    """
    Форма рассылки сообщений для админки
    """
    id_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='/iceman/autocomplete/usersdevice/'),
        label='Пользователь',
        required=False
    )
    advisor = forms.CharField(label=_('Рекомендатель'),
                              widget=forms.TextInput(attrs={'class': 'vLargeTextField'}),
                              required=False)
    status_legal = forms.ChoiceField(label=_('Legal status'),
                                     choices=User.legal_statuses + (('all', _('All')), ), initial='all',
                                     widget=forms.Select(),
                                     required=False)
    user_type = forms.ChoiceField(label=_('Тип пользователя'),
                                     choices=User.types + (('all', _('All')), ), initial='all',
                                     widget=forms.Select(),
                                     required=False)
    iceman_status = forms.ModelChoiceField(
        queryset=UserStatusIceman.objects.all(),
        widget=autocomplete.ModelSelect2(url='/iceman/autocomplete/statusiceman/'),
        label='Статус айсман',
        required=False
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=autocomplete.ModelSelect2(url='/iceman/autocomplete/regions/'),
        label='Регион',
        required=False
    )
    last_order_date = forms.DateTimeField(required=False)
    is_overdue = forms.ChoiceField(label=_('Есть просрочка по любому заказу'),
                                     choices= (('yes', _('Yes')), ('no', _('No')), ('all', _('All')), ), initial='all',
                                     widget=forms.Select(),
                                     required=False)
    title = forms.CharField(label=_('Title'),
                            widget=forms.TextInput(attrs={'class': 'vLargeTextField'}),
                            required=True)
    message = forms.CharField(label=_('Message text'),
                              widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
                              required=True)


class ExportStoresForm(forms.Form):

    types = (('', '---------'), ) + Store.types

    source = forms.ModelChoiceField(queryset=Source.objects.all(), label='Источник')
    region = forms.ModelChoiceField(queryset=Region.objects.all(), label='Регион')
    store_type = forms.ChoiceField(choices=types, label='Тип')


class ExportTasksForm(forms.Form):

    source = forms.ModelChoiceField(queryset=Source.objects.all(), label='Источник')
    task = forms.ModelChoiceField(queryset=Task.objects.filter(application='iceman'), label='Задача')
    region = forms.ModelChoiceField(queryset=Region.objects.all(), label='Регион')
