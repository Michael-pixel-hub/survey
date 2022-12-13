# Generated by Django 2.1 on 2019-01-13 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0010_good_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='agent.Store', verbose_name='For store'),
        ),
        migrations.AlterField(
            model_name='ordergood',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='agent.Store', verbose_name='For store'),
        ),
    ]
