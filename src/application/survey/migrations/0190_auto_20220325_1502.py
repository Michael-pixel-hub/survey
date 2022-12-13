# Generated by Django 2.2.24 on 2022-03-25 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0189_auto_20220325_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='import',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='imports/%Y/%m/%d/', verbose_name='File'),
        ),
        migrations.AddField(
            model_name='import',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey_import_user', to='survey.User', verbose_name='User'),
        ),
    ]
