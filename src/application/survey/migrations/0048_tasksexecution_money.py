# Generated by Django 2.1 on 2019-08-29 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0047_user_is_fixed_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksexecution',
            name='money',
            field=models.FloatField(default=0, verbose_name='Sum'),
        ),
    ]
