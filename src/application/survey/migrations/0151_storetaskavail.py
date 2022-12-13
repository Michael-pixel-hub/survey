# Generated by Django 2.2.24 on 2021-09-14 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0150_smsattempt'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreTaskAvail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_task_id', models.IntegerField(unique=True, verbose_name='Task id')),
                ('task_id', models.IntegerField(verbose_name='Task id')),
                ('store_id', models.IntegerField(verbose_name='Store id')),
                ('store_code', models.CharField(blank=True, max_length=100, verbose_name='Store code')),
                ('store_client_name', models.CharField(max_length=100, verbose_name='Store client name')),
                ('store_category_name', models.CharField(max_length=100, verbose_name='Store category name')),
                ('store_region_name', models.CharField(max_length=100, verbose_name='Store region name')),
                ('store_address', models.TextField(blank=True, max_length=500, verbose_name='Store address')),
                ('store_longitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('store_latitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('only_user_id', models.IntegerField(verbose_name='Only user id')),
                ('is_add_value', models.BooleanField(blank=True, default=False, verbose_name='Is add value')),
                ('add_value', models.FloatField(blank=True, null=True, verbose_name='New value')),
            ],
            options={
                'verbose_name': 'Store task avail',
                'verbose_name_plural': 'Stores tasks avails',
                'db_table': 'chl_stores_tasks_avail',
                'ordering': ['id'],
            },
        ),
    ]