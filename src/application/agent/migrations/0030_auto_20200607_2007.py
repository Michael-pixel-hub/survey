# Generated by Django 2.1 on 2020-06-07 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0029_auto_20200607_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='inn_address',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='store',
            name='inn_director_name',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Director name'),
        ),
        migrations.AddField(
            model_name='store',
            name='inn_director_title',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Director title'),
        ),
        migrations.AddField(
            model_name='store',
            name='inn_full_name',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Organization full name'),
        ),
        migrations.AddField(
            model_name='store',
            name='inn_kpp',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='KPP'),
        ),
        migrations.AddField(
            model_name='store',
            name='inn_name',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Organization name'),
        ),
        migrations.AddField(
            model_name='store',
            name='inn_ogrn',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='OGRN'),
        ),
        migrations.AddField(
            model_name='store',
            name='inn_okved',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='OKVED'),
        ),
    ]
