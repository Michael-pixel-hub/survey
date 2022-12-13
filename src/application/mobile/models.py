from application.survey.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


categories = (
    ('important', _('Important message')),
    ('task', _('Task')),
    ('act', _('Act')),
)


class Notification(models.Model):

    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, null=True, blank=True)
    date_create = models.DateTimeField(_('Date create'), auto_now_add=True)
    title = models.CharField(_('Title'), max_length=255)
    message = models.TextField(_('Message'))
    category = models.TextField(_('Category'), max_length=20, default='important', choices=categories)

    is_sent = models.BooleanField(_('Is sent'), default=False)

    result = models.TextField(_('Result'), default='', blank=True)

    class Meta:
        db_table = 'mobile_notifications'
        ordering = ['-date_create']
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return '%s #%s' % (_('Notification'), self.id)
