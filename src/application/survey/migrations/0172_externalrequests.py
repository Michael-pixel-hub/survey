# Generated by Django 2.2.24 on 2021-12-29 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0171_auto_20211227_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(auto_now_add=True, verbose_name='Request date')),
                ('request_method', models.CharField(blank=True, default='', max_length=1000, verbose_name='Request method')),
                ('request_type', models.CharField(blank=True, default='', max_length=1000, verbose_name='Request type')),
                ('request_ip', models.CharField(blank=True, default='', max_length=1000, verbose_name='Request ip')),
                ('request_text', models.TextField(blank=True, default='', verbose_name='Request text')),
                ('request_files', models.TextField(blank=True, default='', verbose_name='Request files')),
                ('request_data_type', models.CharField(blank=True, default='', max_length=100, verbose_name='Request data type')),
                ('request_data_count', models.IntegerField(blank=True, null=True, verbose_name='Request data count')),
                ('processed', models.BooleanField(default=False, verbose_name='Processed')),
                ('result', models.TextField(blank=True, default='', verbose_name='Result')),
            ],
            options={
                'verbose_name': 'External request',
                'verbose_name_plural': 'External requests',
                'db_table': 'survey_requests_external',
                'ordering': ['-request_date'],
            },
        ),
    ]