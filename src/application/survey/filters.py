from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter

from .models import Task, Rank


class UserRankFilter(MultipleChoiceListFilter):
    title = _('Exclude rank')
    parameter_name = 'user__rank__in'

    def lookups(self, request, model_admin):
        ranks = Rank.objects.all()
        return [(str(i.id), i.name) for i in ranks]

    def queryset(self, request, queryset):
        if request.GET.get(self.parameter_name):
            kwargs = {self.parameter_name: request.GET[self.parameter_name].split(',')}
            queryset = queryset.exclude(**kwargs)
        return queryset


class CodeFilter(SimpleListFilter):
    title = _('Code')

    parameter_name = 'code'

    def lookups(self, request, model_admin):
        return (
            (None, _('All')),
            ('msk', _('Moscow')),
            ('spb', _('Saint Petersburg')),
            ('other', _('Other')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):

        if self.value() == 'spb':
            return queryset.filter(store__code__istartswith='СПБ')
        if self.value() == 'msk':
            return queryset.filter(store__code__istartswith='МСК')
        if self.value() == 'other':
            return queryset.exclude(store__code__istartswith='СПБ').exclude(store__code__istartswith='МСК')
        return queryset


class TaskFilter(SimpleListFilter):

    title = _('Task')

    parameter_name = 'task'

    def lookups(self, request, model_admin):
        tasks = Task.objects.all()
        if not request.user.is_superuser and request.user.task:
            tasks = tasks.filter(id__in=request.user.task.values_list('id', flat=True))
        return [(None, _('All'))] + [(str(i.id), i.name) for i in tasks]

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(task__id=self.value())


class InputFilter(SimpleListFilter):

    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class RegionFilter(InputFilter):

    parameter_name = 'region'
    title = _('Region')

    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(store__region_o__name__icontains=bit) |
                Q(store__region__icontains=bit)
            )
        return queryset.filter(any_name)


class ClientFilter(InputFilter):

    parameter_name = 'client'
    title = _('Client')

    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return
        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(store__client__name__icontains=bit)
            )
        return queryset.filter(any_name)
