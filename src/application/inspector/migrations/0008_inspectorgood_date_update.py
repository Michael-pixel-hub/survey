# Generated by Django 2.1 on 2020-05-15 15:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inspector', '0007_inspectorgood'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectorgood',
            name='date_update',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date update'),
            preserve_default=False,
        ),
    ]
