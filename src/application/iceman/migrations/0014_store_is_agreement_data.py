# Generated by Django 2.2.24 on 2022-02-05 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0013_remove_storetask_is_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_agreement_data',
            field=models.BooleanField(default=False, verbose_name='Данные для договора'),
        ),
    ]
