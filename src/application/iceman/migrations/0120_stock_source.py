# Generated by Django 2.2.28 on 2022-11-15 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0119_auto_20221112_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iceman.Source', verbose_name='Источник'),
        ),
    ]