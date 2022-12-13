# Generated by Django 2.2.24 on 2022-03-24 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0186_auto_20220228_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='fix_status',
            field=models.BooleanField(default=False, help_text='Задачи с фиксированным статусом невозможно менять в интерфейсе администрирования', verbose_name='Фиксировать статус'),
        ),
    ]
