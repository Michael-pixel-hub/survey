# Generated by Django 2.2.16 on 2020-10-21 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0046_auto_20201018_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='from_1c_cashback',
            field=models.FloatField(blank=True, null=True, verbose_name='1c cashback'),
        ),
    ]
