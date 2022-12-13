from django.db import models
from django.utils.translation import ugettext_lazy as _


class Good(models.Model):

    name = models.CharField(_('Name'), max_length=100)
    sku_id = models.IntegerField(_('Sku id'), unique=True)
    date_update = models.DateTimeField(_('Date update'), auto_now_add=True)
    cid = models.CharField(_('Customer id'), null=True, blank=True, max_length=100)

    class Meta:
        db_table = 'inspector_goods'
        ordering = ['name']
        verbose_name = _('Inspector good')
        verbose_name_plural = _('Inspector goods')

    def __str__(self):
        return '%s' % self.name


class Manufacturer(models.Model):

    name = models.TextField(_('Name'))
    internal_id = models.IntegerField(_('Internal id'), unique=True)
    date_update = models.DateTimeField(_('Date update'), auto_now_add=True)

    class Meta:
        db_table = 'inspector_manufacturers'
        ordering = ['name']
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')

    def __str__(self):
        return '%s' % self.name


class Brand(models.Model):

    name = models.TextField(_('Name'))
    internal_id = models.IntegerField(_('Internal id'), unique=True)
    date_update = models.DateTimeField(_('Date update'), auto_now_add=True)

    class Meta:
        db_table = 'inspector_brands'
        ordering = ['name']
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return '%s' % self.name


class Category(models.Model):

    name = models.TextField(_('Name'))
    internal_id = models.IntegerField(_('Internal id'), unique=True)
    date_update = models.DateTimeField(_('Date update'), auto_now_add=True)

    class Meta:
        db_table = 'inspector_categories'
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return '%s' % self.name


class InspectorGood(models.Model):

    name = models.TextField(_('Name'))
    cid = models.CharField(_('Customer id'), null=True, blank=True, max_length=100)
    sku_id = models.IntegerField(_('Sku id'), unique=True)
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_('Manufacturer'), on_delete=models.CASCADE, null=True,
                                     blank=True)
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), on_delete=models.CASCADE, null=True, blank=True)
    date_update = models.DateTimeField(_('Date update'), auto_now_add=True)

    class Meta:
        db_table = 'inspector_all_goods'
        ordering = ['name']
        verbose_name = _('Inspector good')
        verbose_name_plural = _('Inspector goods')

    def __str__(self):
        return '%s' % self.name
