# Generated by Django 2.1 on 2019-01-23 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0018_goodprice'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='goodprice',
            unique_together={('good', 'city')},
        ),
    ]
