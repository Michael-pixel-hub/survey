# Generated by Django 2.2.24 on 2022-04-13 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0196_bank'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bank',
            options={'ordering': ['name'], 'verbose_name': 'Банк', 'verbose_name_plural': 'Банки'},
        ),
    ]
