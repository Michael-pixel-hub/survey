# Generated by Django 2.1 on 2018-11-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_tasksexecution_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_sales',
            field=models.BooleanField(blank=True, default=False, verbose_name='Is sales task'),
        ),
    ]