# Generated by Django 2.2.28 on 2022-07-21 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0228_auto_20220718_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(blank=True, choices=[('supervisor', 'Супервайзер')], max_length=100, null=True, verbose_name='Тип пользователя'),
        ),
    ]
