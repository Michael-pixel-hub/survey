# Generated by Django 2.2.24 on 2022-04-23 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0198_user_taxpayer_bank'),
        ('iceman', '0090_auto_20220415_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='iceman_store_user', to='survey.User', verbose_name='Пользователь'),
        ),
    ]
