# Generated by Django 2.2.24 on 2021-09-14 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0151_storetaskavail'),
    ]

    operations = [
        migrations.AddField(
            model_name='storetaskavail',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is delete'),
        ),
    ]