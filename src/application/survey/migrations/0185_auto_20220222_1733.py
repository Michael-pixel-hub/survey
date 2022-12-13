# Generated by Django 2.2.24 on 2022-02-22 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0184_auto_20220222_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksexecution',
            name='check_type',
            field=models.CharField(choices=[('not_verified', 'Not verified'), ('true', 'Correct check'), ('false', 'Incorrect check'), ('not_need', 'Не нужно')], default='not_need', max_length=12, verbose_name='Check'),
        ),
    ]