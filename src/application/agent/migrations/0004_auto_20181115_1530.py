# Generated by Django 2.1 on 2018-11-15 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0003_store'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={'ordering': ['-date_create'], 'verbose_name': 'Store', 'verbose_name_plural': 'Stores'},
        ),
    ]
