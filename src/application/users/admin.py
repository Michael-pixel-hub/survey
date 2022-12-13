from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _

from public_model.admin import active_model

from .models import User


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        return password2

    def save(self, commit=True):

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"

    def clean_password(self):
        return self.initial["password"]


@active_model
class UserAdmin(BaseUserAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'user_permissions':
            kwargs['queryset'] = Permission.objects.all().select_related('content_type')
        return super(UserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'date_joined', 'last_login', 'is_staff', 'is_superuser', )

    fieldsets = (
        (None, {
            'fields': ('email', 'password', )
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions', )
        }),
        ('Клиентский раздел Сюрвеер', {
            'fields': ('task', 'show_date_end')
        }),
        ('Клиентский раздел Айсмен', {
            'fields': ('sources', )
        }),
        (_('Important dates'), {
            'fields': ('date_joined', 'last_login', )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', )
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions', 'task', 'sources', )
    list_filter = ('is_staff', 'is_superuser', )
    readonly_fields = ('date_joined', )


admin.site.register(User, UserAdmin)
