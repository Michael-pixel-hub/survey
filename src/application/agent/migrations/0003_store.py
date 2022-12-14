# Generated by Django 2.1 on 2018-11-13 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_tasksexecution_comments'),
        ('agent', '0002_import'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Date create')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('contact', models.CharField(max_length=255, verbose_name='Contact face')),
                ('phone', models.CharField(max_length=30, verbose_name='Phone')),
                ('address', models.CharField(max_length=1000, verbose_name='Address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.User', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Data import',
                'verbose_name_plural': 'Data imports',
                'db_table': 'agent_stores',
                'ordering': ['-date_create'],
            },
        ),
    ]
