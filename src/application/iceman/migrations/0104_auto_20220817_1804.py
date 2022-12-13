# Generated by Django 2.2.28 on 2022-08-17 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0231_task_ai_project'),
        ('iceman', '0103_storetaskschedule'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storetask',
            options={'ordering': ['store_id'], 'verbose_name': 'Задача в магазине', 'verbose_name_plural': 'Задачи в магазинах сегодня'},
        ),
        migrations.AlterUniqueTogether(
            name='storetaskschedule',
            unique_together={('store', 'task')},
        ),
    ]