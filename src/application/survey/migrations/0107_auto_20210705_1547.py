# Generated by Django 2.2.20 on 2021-07-05 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0106_act_date_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Date update'),
        ),
    ]