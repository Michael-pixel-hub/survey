# Generated by Django 2.2.24 on 2021-11-30 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0166_userdevice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdevice',
            name='key',
            field=models.CharField(max_length=255, verbose_name='Device key'),
        ),
    ]
