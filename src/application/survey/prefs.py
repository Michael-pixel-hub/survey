from preferences.registry import preferences, StringPreference, NumberPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class StoreSearchRadius(NumberPreference):
    name = _('Store search radius')
    category = _('Chistaya liniya')


@preferences.register
class RestrictOtherSum(NumberPreference):
    name = _('Maximum year amount of tasks for non-self-employed')
    category = _('Chistaya liniya')
    default = 15000

