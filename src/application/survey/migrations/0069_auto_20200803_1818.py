# Generated by Django 2.2.14 on 2020-08-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0068_auto_20200608_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadrequests',
            name='processed',
            field=models.BooleanField(default=False, verbose_name='Processed'),
        ),
        migrations.AddField(
            model_name='uploadrequests',
            name='result',
            field=models.TextField(blank=True, default='', verbose_name='Result'),
        ),
    ]