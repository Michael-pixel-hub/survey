# Generated by Django 2.1 on 2019-06-21 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0033_good_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Code'),
        ),
    ]
