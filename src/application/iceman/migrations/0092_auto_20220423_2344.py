# Generated by Django 2.2.24 on 2022-04-23 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0091_store_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Код'),
        ),
    ]
