# Generated by Django 2.2.24 on 2022-01-24 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0003_auto_20220124_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='storetask',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Время обновления'),
        ),
    ]
