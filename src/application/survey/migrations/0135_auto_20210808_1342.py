# Generated by Django 2.2.24 on 2021-08-08 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0134_tasksexecutionquestionnaire_questionnaire'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasksexecutionquestionnaire',
            name='question_text',
        ),
        migrations.RemoveField(
            model_name='tasksexecutionquestionnaire',
            name='questionnaire',
        ),
        migrations.AddField(
            model_name='tasksexecutionquestionnaire',
            name='constructor_step_name',
            field=models.CharField(default='', max_length=200, verbose_name='Step name'),
        ),
        migrations.AddField(
            model_name='tasksexecutionquestionnaire',
            name='name',
            field=models.CharField(default='', max_length=200, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tasksexecutionquestionnaire',
            name='question',
            field=models.CharField(max_length=1000, verbose_name='Question text'),
        ),
    ]
