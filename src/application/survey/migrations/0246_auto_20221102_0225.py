# Generated by Django 2.2.28 on 2022-11-02 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0245_tasksexecution_is_api_direct'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksexecution',
            name='source_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название устройства'),
        ),
        migrations.AddField(
            model_name='tasksexecution',
            name='source_os',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Операционная система'),
        ),
        migrations.AddField(
            model_name='tasksexecution',
            name='source_os_version',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Версия ОС'),
        ),
        migrations.AddField(
            model_name='tasksexecution',
            name='source_version',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Версия приложения'),
        ),
    ]
