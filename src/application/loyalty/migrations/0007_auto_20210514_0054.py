# Generated by Django 2.2.20 on 2021-05-14 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0006_auto_20210513_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Name'),
        ),
    ]
