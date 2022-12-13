# Generated by Django 2.1 on 2019-06-17 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0031_auto_20190617_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksexecution',
            name='inspector_status',
            field=models.CharField(choices=[('undefined', 'Undefined'), ('wait', 'Waiting for inspector'), ('upload_error', 'Upload error'), ('parse_error', 'Parse error'), ('report_error', 'Report error'), ('report_wait', 'Report waiting'), ('error', 'Error'), ('success', 'Success parsing')], default='wait', max_length=20, verbose_name='Inspector status'),
        ),
    ]
