# Generated by Django 2.2.20 on 2021-07-09 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0111_auto_20210707_1237'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assortment',
            unique_together={('good', 'store', 'task')},
        ),
    ]
