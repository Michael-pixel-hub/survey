# Generated by Django 2.1 on 2018-12-20 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_auto_20181220_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksexecution',
            name='distance',
            field=models.FloatField(blank=True, help_text='Meters', null=True, verbose_name='Distance to store'),
        ),
    ]
