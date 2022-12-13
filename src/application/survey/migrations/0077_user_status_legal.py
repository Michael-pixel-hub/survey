# Generated by Django 2.2.20 on 2021-04-27 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0076_auto_20210424_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status_legal',
            field=models.CharField(choices=[('self_employed', 'Self-employed'), ('other', 'Other')], default='other', max_length=100),
        ),
    ]
