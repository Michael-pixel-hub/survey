# Generated by Django 2.2.28 on 2022-11-14 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0250_user_worker_bonus_iceman'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='factory_code',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Код завода'),
        ),
    ]
