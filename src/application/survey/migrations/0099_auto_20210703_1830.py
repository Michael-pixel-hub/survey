# Generated by Django 2.2.20 on 2021-07-03 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0098_auto_20210703_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='check_type',
            field=models.CharField(choices=[('new', 'New act'), ('wait', 'Waiting for verify'), ('true', 'Correct check'), ('false', 'Incorrect check')], default='new', max_length=12, verbose_name='Check'),
        ),
    ]
