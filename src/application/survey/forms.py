from django import forms
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

from .models import Task, Category, Region, TaskStep, User, Client


class ImportForm(forms.Form):

    assortment_types = (
        ('store', _('Store')),
        ('task', _('Task')),
    )

    file = forms.FileField(label=_('Xls-file'))
    delete_assortment = forms.BooleanField(label=_('Delete assortment'), required=False, initial=False)
    assortment_type = forms.ChoiceField(label=_('Assign assortment to'), required=False, choices=assortment_types,
                                        initial='store', widget=forms.RadioSelect)


class ExportForm(forms.Form):

    TASKS_VALUES = (
        ('all', _('All stores')),
    )
    tasks = forms.ModelChoiceField(queryset=Task.objects.all(), label=_('Task'), initial='all', widget=forms.Select(),
                                   required=False)
    CATEGORIES_VALUES = (
        ('all', _('All categories')),
    )
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), label=_('Category'), initial='all',
                                        widget=forms.Select(), required=False)

    REGIONS_VALUES = (
        ('all', _('All regions')),
    )
    regions = forms.ModelChoiceField(queryset=Region.objects.all(), label=_('Region'), initial='all',
                                     widget=forms.Select(), required=False)


class TaskStepForm(forms.ModelForm):

    class Meta:
        model = TaskStep
        fields = ('__all__')
        widgets = {
            'photo_inspector': forms.Select(choices=((True, _('Yes')), (False, _('No')))),
            'photo_check_assortment': forms.Select(choices=((True, _('Yes')), (False, _('No')))),
            'photo_check': forms.Select(choices=((True, _('Yes')), (False, _('No')))),
            'photo_from_gallery': forms.Select(choices=((True, _('Yes')), (False, _('No')))),
            'photo_out_reason': forms.Select(choices=((True, _('Yes')), (False, _('No')))),
            'photo_out_requires': forms.Select(choices=((True, _('Yes')), (False, _('No')))),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
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


class ImportTasksForm(forms.Form):

    file = forms.FileField(label=_('Xls-file'))


class UploadImageForm(forms.Form):

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('User'),
        widget=autocomplete.ModelSelect2(
                url='survey:ac-users',
                attrs={
                    'data-placeholder': _('Выберите пользователя'),
                },
        ),
        required=False
    )

    task = forms.ModelChoiceField(
        queryset=Task.objects.all(),
        label=_('Task'),
        widget=autocomplete.ModelSelect2(
                url='survey:ac-tasks',
                attrs={
                    'data-placeholder': _('Выберите задачу'),
                },
        ),
        required=False
    )

    imagestep = forms.ModelChoiceField(
        queryset=TaskStep.objects.all(),
        label=_('Task step'),
        initial='',
        widget=autocomplete.ModelSelect2(
                url='survey:ac-imagestep',
                forward=['task'],
                attrs={
                    'data-placeholder': _('Выберите шаг'),
                },
            ),
        required=False
    )

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label=_('Сеть'),
        widget=autocomplete.ModelSelect2(
                url='survey:ac-clients',
                attrs={
                    'data-placeholder': _('Выберите сеть'),
                },
        ),
        required=False
    )
