# Generated by Django 2.2.28 on 2022-10-04 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0113_auto_20220913_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_entry',
            field=models.BooleanField(blank=True, null=True, verbose_name='Не провод'),
        ),
    ]