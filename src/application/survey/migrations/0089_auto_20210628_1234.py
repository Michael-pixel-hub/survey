# Generated by Django 2.2.20 on 2021-06-28 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0088_auto_20210628_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksexecution',
            name='check_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='survey_tasksexecution_check_user', to=settings.AUTH_USER_MODEL, verbose_name='Check user'),
        ),
        migrations.AlterField(
            model_name='tasksexecution',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='survey_tasksexecution_store', to='survey.Store', verbose_name='Store'),
        ),
        migrations.AlterField(
            model_name='tasksexecution',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_tasksexecution_task', to='survey.Task', verbose_name='Task'),
        ),
        migrations.AlterField(
            model_name='tasksexecution',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_tasksexecution_user', to='survey.User', verbose_name='User'),
        ),
    ]