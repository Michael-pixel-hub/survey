# Generated by Django 2.2.28 on 2022-11-02 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0246_auto_20221102_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdevice',
            name='os_version',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Версия ОС'),
        ),
    ]
