# Generated by Django 2.2.20 on 2021-05-16 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0008_auto_20210515_2239'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmentmenuitem',
            options={'ordering': ['department__name', 'order'], 'verbose_name': 'Loyalty department menu item', 'verbose_name_plural': 'Loyalty departments menu items'},
        ),
    ]
