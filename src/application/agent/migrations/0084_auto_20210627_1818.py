# Generated by Django 2.2.20 on 2021-06-27 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0083_auto_20210627_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='store',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promo_codes_stores', to='agent.Store', verbose_name='Store'),
        ),
    ]
