# Generated by Django 2.2.24 on 2021-09-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0149_auto_20210906_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=100, unique=True, verbose_name='Phone')),
                ('attempts', models.IntegerField(default=0, verbose_name='Attempts count')),
            ],
            options={
                'verbose_name': 'Sms attempt',
                'verbose_name_plural': 'Sms attempts',
                'db_table': 'survey_sms_attempts',
                'ordering': ['id'],
            },
        ),
    ]