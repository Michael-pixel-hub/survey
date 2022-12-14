# Generated by Django 2.1 on 2019-01-13 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0011_auto_20190113_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comments_status',
            field=models.TextField(blank=True, default='', help_text='What comes to the user when the status changes', null=True, verbose_name='Status comments'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'New'), (2, 'Payed'), (3, 'Pay in Solar'), (4, 'Not payed'), (5, 'Finished')], default=1, verbose_name='Status'),
        ),
    ]
