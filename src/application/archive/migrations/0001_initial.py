# Generated by Django 2.2.20 on 2021-06-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveTasksExecution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.FloatField(default=0, verbose_name='Sum')),
                ('money_source', models.FloatField(default=0, verbose_name='Sum source')),
                ('date_end', models.DateTimeField(blank=True, null=True, verbose_name='Date end')),
                ('date_end_user', models.DateTimeField(blank=True, null=True, verbose_name='Date end user')),
                ('status', models.IntegerField(choices=[(1, 'Started'), (2, 'Finished'), (3, 'Checked'), (6, 'Pay in Solar'), (4, 'Payed'), (5, 'Denied'), (7, 'Not payed'), (8, 'Temp denied')], default=1, verbose_name='Status')),
                ('image', models.FileField(blank=True, null=True, upload_to='tasks/exec/%Y/%m/%d/', verbose_name='Confirmation image')),
                ('comments', models.TextField(blank=True, default='', help_text='What the user writes', verbose_name='Comments')),
                ('comments_status', models.TextField(blank=True, default='', help_text='What comes to the user when the status changes', null=True, verbose_name='Status comments')),
                ('comments_internal', models.TextField(blank=True, default='', help_text='Remains in the system and is visible only to administrators.', null=True, verbose_name='Internal comments')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('distance', models.FloatField(blank=True, help_text='Meters', null=True, verbose_name='Distance to store')),
                ('step', models.CharField(choices=[('before', 'Photo before'), ('after', 'Photo after'), ('check', 'Photo check'), ('uploaded', 'All photo uploaded')], default='before', max_length=10, verbose_name='Step')),
                ('check_type', models.CharField(choices=[('not_verified', 'Not verified'), ('true', 'Correct check'), ('false', 'Incorrect check')], default='not_verified', max_length=12, verbose_name='Check')),
                ('set_check_verified', models.BooleanField(blank=True, default=False, verbose_name='Set check verified')),
                ('set_check_not_verified', models.BooleanField(blank=True, default=False, verbose_name='Set check not verified')),
                ('is_auditor', models.BooleanField(blank=True, default=False, verbose_name='Checked by auditor')),
                ('inspector_upload_images_text', models.TextField(blank=True, default='', verbose_name='Upload images message')),
                ('inspector_error', models.TextField(blank=True, default='', null=True, verbose_name='Error text')),
                ('inspector_recognize_text', models.TextField(blank=True, default='', null=True, verbose_name='Recognize message')),
                ('inspector_report_text', models.TextField(blank=True, default='', null=True, verbose_name='Report')),
                ('inspector_positions_text', models.TextField(blank=True, default='', null=True, verbose_name='Positions text')),
                ('inspector_status', models.CharField(choices=[('undefined', 'Undefined'), ('wait', 'Waiting for inspector'), ('upload_wait', 'Upload wait'), ('upload_error', 'Upload error'), ('parse_error', 'Parse error'), ('report_process', 'Report process'), ('report_error', 'Report error'), ('report_wait', 'Report waiting'), ('error', 'Error'), ('success', 'Success parsing')], default='wait', max_length=20, verbose_name='Inspector status')),
                ('inspector_report_id', models.IntegerField(blank=True, null=True, verbose_name='Report id')),
                ('inspector_report_id_before', models.IntegerField(blank=True, null=True, verbose_name='Report id before')),
                ('inspector_status_before', models.CharField(choices=[('undefined', 'Undefined'), ('wait', 'Waiting for inspector'), ('upload_wait', 'Upload wait'), ('upload_error', 'Upload error'), ('parse_error', 'Parse error'), ('report_process', 'Report process'), ('report_error', 'Report error'), ('report_wait', 'Report waiting'), ('error', 'Error'), ('success', 'Success parsing')], default='wait', max_length=20, verbose_name='Inspector status before')),
                ('inspector_is_alert', models.BooleanField(blank=True, default=False, verbose_name='Inspector alert')),
                ('inspector_re_work', models.BooleanField(blank=True, default=False, verbose_name='Inspector re work')),
                ('inspector_is_work', models.BooleanField(blank=True, default=False, verbose_name='Inspector is work')),
                ('telegram_channel_status', models.IntegerField(choices=[(0, 'Not need'), (1, 'Wait'), (2, 'Sent')], default=0, verbose_name='Telegram channel status')),
                ('date_start', models.DateTimeField(verbose_name='Date start')),
            ],
            options={
                'verbose_name': 'Task execution [archive]',
                'verbose_name_plural': 'Tasks execution [archive]',
                'db_table': 'archive_tasks_executions',
                'ordering': ['-date_start'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ArchiveTasksExecutionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, db_index=True, null=True, upload_to='tasks/exec/%Y/%m/%d/', verbose_name='Image')),
                ('status', models.CharField(db_index=True, default='Анализ изображения в процессе...', max_length=1000, verbose_name='Unique status')),
                ('md5', models.CharField(blank=True, max_length=32, null=True, verbose_name='Md5 sum')),
                ('type', models.CharField(choices=[('undefined', 'Undefined'), ('enter', 'Enter photo'), ('before', 'Photo before work'), ('after', 'Photo after work'), ('check', 'Cass check')], default='undefined', max_length=10, verbose_name='Image type')),
                ('telegram_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Telegram id')),
            ],
            options={
                'db_table': 'archive_tasks_executions_images',
                'managed': False,
            },
        ),
    ]