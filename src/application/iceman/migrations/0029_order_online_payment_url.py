# Generated by Django 2.2.24 on 2022-02-12 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0028_auto_20220212_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='online_payment_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Url платежа'),
        ),
    ]
