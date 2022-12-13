# Generated by Django 2.2.24 on 2022-02-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0183_task_money_fix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksexecution',
            name='check_type',
            field=models.CharField(choices=[('not_verified', 'Not verified'), ('true', 'Correct check'), ('false', 'Incorrect check'), ('not_need', 'Не нужно')], default='not_verified', max_length=12, verbose_name='Check'),
        ),
    ]