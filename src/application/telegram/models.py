from application.survey.models import User

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cache_model.models import CacheModel
from public_model.models import PublicModel
from sort_model.models import OrderModel

SHORT_VALUE_LENGTH = 100


class String(CacheModel, models.Model):
    """
    Текстовые сообщения и кнопки. Любые текстовые элементы бота
    """

    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('System name'), max_length=100, unique=True)
    category = models.CharField(_('Category'), max_length=255)
    value = models.TextField(_('Value'), max_length=1000, help_text=_('Formatting telegram message'))

    object = models.Manager()

    class Meta:
        db_table = 'telegram_strings'
        ordering = ['category', 'name']
        verbose_name = _('Telegram message/button')
        verbose_name_plural = _('Telegram messages/buttons')

    def __str__(self):
        return '%s' % self.name

    @staticmethod
    def get_string(name):

        try:
            return String.objects.get(slug=name).value
        except String.DoesNotExist:
            return ''

    def print_value(self):
        s = self.value[:SHORT_VALUE_LENGTH-3]
        if len(self.value) > SHORT_VALUE_LENGTH:
            s += '...'
        return s
    print_value.short_description = _('Value')


class Menu(CacheModel, OrderModel, PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=100, unique=True)
    value = models.TextField(_('Value'), help_text=_('Formatting telegram message'))

    object = models.Manager()

    class Meta:
        db_table = 'telegram_menu'
        ordering = ['order']
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu')

    def __str__(self):
        return '%s' % self.name


class Channel(PublicModel, models.Model):

    name = models.CharField(_('Name'), max_length=200)
    telegram_id = models.CharField(_('Telegram id'), unique=True, max_length=100)

    class Meta:
        db_table = 'telegram_channels'
        ordering = ['name']
        verbose_name = _('Telegram channel')
        verbose_name_plural = _('Telegram channels')

    def __str__(self):
        return '%s' % self.name


class Process(models.Model):

    user = models.OneToOneField(User, verbose_name=_('User'), on_delete=models.CASCADE)
    module = models.CharField(_('Module'), max_length=255)
    function = models.CharField(_('Function'), max_length=255)

    class Meta:
        db_table = 'telegram_process'
        ordering = ['user__username']
        verbose_name = _('Process')
        verbose_name_plural = _('Process')

    def __str__(self):
        return '%s' % self.user.username


class ProcessAttr(models.Model):

    procedure = models.ForeignKey(Process, verbose_name=_('Process'), on_delete=models.CASCADE)
    value = models.TextField(_('Value'), max_length=1000)

    class Meta:
        db_table = 'telegram_process_attrs'
        ordering = ['procedure__id', 'id']
        verbose_name = _('Process attribute')
        verbose_name_plural = _('Process attributes')

    def __str__(self):
        return '%s' % self.value
