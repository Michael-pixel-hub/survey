# Generated by Django 2.2.20 on 2021-06-16 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0063_auto_20210615_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='agent',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Sales Representative'),
        ),
    ]
