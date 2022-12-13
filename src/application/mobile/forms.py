from django import forms
from django.utils.translation import ugettext_lazy as _
from dal import autocomplete

from application.survey.models import User, UserStatus, Rank


class MessageForm(forms.Form):
    """
    Форма рассылки сообщений для админки
    """
    id_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='/survey/autocomplete/usersdevice/'),
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
    user_status = forms.ModelChoiceField(
        queryset=UserStatus.objects.all(),
        widget=autocomplete.ModelSelect2(url='/survey/autocomplete/userstatus/'),
        label='Статус сюрвеера',
        required=False
    )
    rank = forms.ModelChoiceField(
        queryset=Rank.objects.all(),
        widget=autocomplete.ModelSelect2(url='/survey/autocomplete/ranks/'),
        label='Рейтинг',
        required=False
    )
    title = forms.CharField(label=_('Title'),
                            widget=forms.TextInput(attrs={'class': 'vLargeTextField'}),
                            required=True)
    message = forms.CharField(label=_('Message text'),
                              widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
                              required=True)
