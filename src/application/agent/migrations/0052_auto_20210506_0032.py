# Generated by Django 2.2.20 on 2021-05-06 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0001_initial'),
        ('agent', '0051_auto_20201028_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='loyalty_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loyalty.Department', verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='store',
            name='loyalty_program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loyalty.Program', verbose_name='Loyalty program'),
        ),
    ]
