# Generated by Django 2.1 on 2018-08-23 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_join'], 'verbose_name': 'Telegram user', 'verbose_name_plural': 'Telegram users'},
        ),
        migrations.AlterField(
            model_name='tasksexecutionimage',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_images', to='survey.TasksExecution', verbose_name='Task execution'),
        ),
    ]
