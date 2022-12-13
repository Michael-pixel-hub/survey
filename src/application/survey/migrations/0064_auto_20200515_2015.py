# Generated by Django 2.1 on 2020-05-15 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0063_auto_20200515_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksexecution',
            name='inspector_status',
            field=models.CharField(choices=[('undefined', 'Undefined'), ('wait', 'Waiting for inspector'), ('upload_wait', 'Upload wait'), ('upload_error', 'Upload error'), ('parse_error', 'Parse error'), ('report_process', 'Report process'), ('report_error', 'Report error'), ('report_wait', 'Report waiting'), ('error', 'Error'), ('success', 'Success parsing')], default='wait', max_length=20, verbose_name='Inspector status'),
        ),
        migrations.AlterField(
            model_name='tasksexecution',
            name='inspector_status_before',
            field=models.CharField(choices=[('undefined', 'Undefined'), ('wait', 'Waiting for inspector'), ('upload_wait', 'Upload wait'), ('upload_error', 'Upload error'), ('parse_error', 'Parse error'), ('report_process', 'Report process'), ('report_error', 'Report error'), ('report_wait', 'Report waiting'), ('error', 'Error'), ('success', 'Success parsing')], default='wait', max_length=20, verbose_name='Inspector status before'),
        ),
    ]
