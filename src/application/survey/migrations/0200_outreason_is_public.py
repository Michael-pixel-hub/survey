# Generated by Django 2.2.28 on 2022-05-03 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0199_outreason'),
    ]

    operations = [
        migrations.AddField(
            model_name='outreason',
            name='is_public',
            field=models.BooleanField(default=True, verbose_name='Is public'),
        ),
    ]
