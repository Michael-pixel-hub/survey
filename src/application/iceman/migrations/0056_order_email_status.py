# Generated by Django 2.2.24 on 2022-03-04 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0055_auto_20220304_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email_status',
            field=models.CharField(choices=[('no_need', 'Не нужно'), ('wait', 'Ожидание'), ('sent', 'Отправлено')], default='no_need', max_length=20, verbose_name='Статус email'),
        ),
    ]
