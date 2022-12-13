# Generated by Django 2.2.24 on 2022-03-25 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0190_auto_20220325_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='import',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey_import_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
