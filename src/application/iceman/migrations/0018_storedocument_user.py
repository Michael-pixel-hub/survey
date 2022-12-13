# Generated by Django 2.2.24 on 2022-02-10 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0182_task_type'),
        ('iceman', '0017_auto_20220210_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='storedocument',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='iceman_store_document_user', to='survey.User', verbose_name='Пользователь'),
        ),
    ]