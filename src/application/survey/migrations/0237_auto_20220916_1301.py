# Generated by Django 2.2.28 on 2022-09-16 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0236_auto_20220916_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penalty',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='survey_penalty_creator', to=settings.AUTH_USER_MODEL, verbose_name='Координатор'),
        ),
    ]
