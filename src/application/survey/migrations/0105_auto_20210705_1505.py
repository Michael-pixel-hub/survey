# Generated by Django 2.2.20 on 2021-07-05 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0104_auto_20210705_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='id_1c',
            field=models.CharField(max_length=255, unique=True, verbose_name='1c id'),
        ),
    ]
