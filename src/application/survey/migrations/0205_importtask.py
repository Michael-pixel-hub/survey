# Generated by Django 2.2.24 on 2022-05-14 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0204_auto_20220507_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255, verbose_name='File name')),
                ('date_start', models.DateTimeField(auto_now_add=True, verbose_name='Date start')),
                ('date_end', models.DateTimeField(blank=True, null=True, verbose_name='Date end')),
                ('rows_count', models.IntegerField(blank=True, null=True, verbose_name='Rows count')),
                ('rows_process', models.IntegerField(blank=True, default=0, verbose_name='Rows process')),
                ('status', models.IntegerField(choices=[(1, 'In process'), (2, 'Finished'), (3, 'Canceled'), (4, 'Error')], default=1, verbose_name='Status')),
                ('report_text', models.TextField(blank=True, null=True, verbose_name='Report text')),
                ('file', models.FileField(blank=True, null=True, upload_to='imports/%Y/%m/%d/', verbose_name='File')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey_import_tasks_user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Task import',
                'verbose_name_plural': 'Tasks imports',
                'db_table': 'chl_imports_tasks',
                'ordering': ['-date_start'],
            },
        ),
    ]