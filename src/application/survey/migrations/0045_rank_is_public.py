# Generated by Django 2.1 on 2019-08-29 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0044_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='is_public',
            field=models.BooleanField(default=True, verbose_name='Is public'),
        ),
    ]