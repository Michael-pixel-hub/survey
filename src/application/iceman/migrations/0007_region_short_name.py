# Generated by Django 2.2.24 on 2022-01-26 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0006_auto_20220126_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='short_name',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Короткое название'),
            preserve_default=False,
        ),
    ]
