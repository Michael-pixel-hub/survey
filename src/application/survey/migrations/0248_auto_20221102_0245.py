# Generated by Django 2.2.28 on 2022-11-02 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0247_auto_20221102_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdevice',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='userdevice',
            name='os',
            field=models.CharField(blank=True, max_length=255, verbose_name='OS'),
        ),
        migrations.AlterField(
            model_name='userdevice',
            name='version',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Version'),
        ),
    ]