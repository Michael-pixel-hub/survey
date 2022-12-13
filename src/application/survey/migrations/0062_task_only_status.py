# Generated by Django 2.1 on 2020-04-08 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0061_auto_20200408_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='only_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_user_status', to='survey.UserStatus', verbose_name='Only for user status'),
        ),
    ]
