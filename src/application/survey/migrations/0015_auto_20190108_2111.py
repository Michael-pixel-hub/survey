# Generated by Django 2.1 on 2019-01-08 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0014_auto_20190103_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksexecution',
            name='status',
            field=models.IntegerField(choices=[(1, 'Started'), (2, 'Finished'), (3, 'Checked'), (6, 'Pay in Solar'), (4, 'Payed'), (5, 'Denied'), (7, 'Not payed')], default=1, verbose_name='Status'),
        ),
    ]