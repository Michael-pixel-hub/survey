# Generated by Django 2.2.28 on 2022-05-03 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0200_outreason_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstep',
            name='photo_out_reason',
            field=models.BooleanField(default=False, verbose_name='Указать причины отсутствия'),
        ),
        migrations.AddField(
            model_name='taskstep',
            name='photo_out_requires',
            field=models.BooleanField(default=False, verbose_name='Причины отсутствия обязательны'),
        ),
    ]