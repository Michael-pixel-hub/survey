# Generated by Django 2.2.24 on 2022-04-13 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0197_auto_20220413_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='taxpayer_bank',
            field=models.ForeignKey(blank=True, null=True, on_delete='Банк', to='survey.Bank'),
        ),
    ]
