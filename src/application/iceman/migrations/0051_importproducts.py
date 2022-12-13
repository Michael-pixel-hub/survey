# Generated by Django 2.2.24 on 2022-03-03 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0050_importstores'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255, verbose_name='File name')),
                ('date_start', models.DateTimeField(auto_now_add=True, verbose_name='Date start')),
                ('date_end', models.DateTimeField(blank=True, null=True, verbose_name='Date end')),
                ('rows_count', models.IntegerField(blank=True, null=True, verbose_name='Rows count')),
                ('rows_process', models.IntegerField(blank=True, default=0, verbose_name='Rows process')),
                ('status', models.IntegerField(choices=[(1, 'In process'), (2, 'Finished'), (3, 'Canceled'), (4, 'Error')], default=1, verbose_name='Status')),
                ('report_text', models.TextField(blank=True, null=True, verbose_name='Report text')),
            ],
            options={
                'verbose_name': 'Data import',
                'verbose_name_plural': 'Data imports',
                'db_table': 'iceman_imports_products',
                'ordering': ['-date_start'],
            },
        ),
    ]
