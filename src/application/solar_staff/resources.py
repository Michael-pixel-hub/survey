from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Payment, User, SolarStaffAccount


class UserForeignKeyWidget(ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if value is None or value == '':
            raise Exception(f'E-mail пользователя не может быть пустым!')
        val = self.get_queryset(value, row, *args, **kwargs).filter(**{self.field: value}).last()
        if val is None:
            raise Exception(f'Пользователь с email "{value}" не найден!')
        return val


class SSForeignKeyWidget(ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        if value is None or value == '':
            return None
        try:
            val = self.get_queryset(value, row, *args, **kwargs).get(**{self.field: value})
        except SolarStaffAccount.DoesNotExist:
            raise Exception(f'Solar Staff аккаунт с названием "{value}" не найден!')
        return val


class PaymentResource(resources.ModelResource):

    user = fields.Field(column_name='user', attribute='user', widget=UserForeignKeyWidget(User, 'email'))
    ss_account = fields.Field(column_name='ss_account', attribute='ss_account',
                              widget=SSForeignKeyWidget(SolarStaffAccount, 'name'))

    class Meta:
        model = Payment
        import_id_fields = ('user', 'sum', 'comment',)
        exclude = ('id', 'status', 'date_create', 'date_payment',)
        skip_unchanged = True
        fields = ('user', 'sum', 'comment', 'ss_account', )
