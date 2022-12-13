from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from application.iceman.models import Source
from application.survey.models import Task, Region

from public_model.models import ActiveModel


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):

        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(ActiveModel, PermissionsMixin, AbstractBaseUser):

    """
    User model
    """

    email = models.EmailField(verbose_name=_('E-mail'), max_length=30, unique=True)
    is_staff = models.BooleanField(_('Is staff'), default=False)
    date_joined = models.DateField(_('Date created'), default=datetime.now)

    task = models.ManyToManyField(Task, verbose_name=_('Only view task'), blank=True)
    regions = models.ManyToManyField(Region, verbose_name=_('Regions for reports'), blank=True)
    sources = models.ManyToManyField(Source, verbose_name=_('Source'), blank=True)

    show_date_end = models.BooleanField('Показывать дату завершения заданий', default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'auth_user'
        ordering = ['email']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def username(self):
        return self.email
