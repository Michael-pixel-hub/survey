# Generated by Django 2.1 on 2019-01-09 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0015_auto_20190108_2111'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['address'], name='chl_stores_address_a86103_idx'),
        ),
        migrations.AddIndex(
            model_name='tasksexecution',
            index=models.Index(fields=['comments'], name='chl_tasks_e_comment_7e045d_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='telegram_us_usernam_6569ec_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['first_name'], name='telegram_us_first_n_42ab3c_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['last_name'], name='telegram_us_last_na_925134_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['phone'], name='telegram_us_phone_aa5d63_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['name'], name='telegram_us_name_1d956c_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['surname'], name='telegram_us_surname_4d03e2_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='telegram_us_email_38fcb8_idx'),
        ),
    ]
