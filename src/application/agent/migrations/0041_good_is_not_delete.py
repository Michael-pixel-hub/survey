# Generated by Django 2.2.14 on 2020-09-04 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0040_auto_20200828_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='is_not_delete',
            field=models.BooleanField(default=False, verbose_name='Is bot delete'),
        ),
    ]
