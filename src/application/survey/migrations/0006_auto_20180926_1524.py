# Generated by Django 2.1 on 2018-09-26 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20180923_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksexecution',
            name='status',
            field=models.IntegerField(choices=[(1, 'Started'), (2, 'Finished'), (3, 'Checked'), (4, 'Payed'), (5, 'Denied')], default=1, verbose_name='Status'),
        ),
        migrations.AlterUniqueTogether(
            name='storetask',
            unique_together={('task', 'store')},
        ),
    ]