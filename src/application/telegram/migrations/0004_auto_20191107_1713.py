# Generated by Django 2.1 on 2019-11-07 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0003_channel_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
    ]