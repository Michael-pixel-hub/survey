# Generated by Django 2.1 on 2019-12-23 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0057_auto_20191223_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storetask',
            name='add_value',
            field=models.FloatField(blank=True, null=True, verbose_name='New value'),
        ),
    ]
