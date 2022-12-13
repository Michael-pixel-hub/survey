# Generated by Django 2.1 on 2020-05-21 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0065_tasksexecution_date_end_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(auto_now_add=True, verbose_name='Request date')),
                ('request_method', models.CharField(blank=True, default='', max_length=1000, verbose_name='Request method')),
                ('request_type', models.CharField(blank=True, default='', max_length=1000, verbose_name='Request type')),
                ('request_ip', models.CharField(blank=True, default='', max_length=1000, verbose_name='Request ip')),
                ('request_text', models.TextField(blank=True, default='', verbose_name='Request text')),
                ('request_files', models.TextField(blank=True, default='', verbose_name='Request files')),
            ],
            options={
                'verbose_name': 'Upload request',
                'verbose_name_plural': 'Upload requests',
                'db_table': 'survey_1c_requests',
                'ordering': ['-request_date'],
            },
        ),
    ]
