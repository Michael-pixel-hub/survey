# Generated by Django 2.2.20 on 2021-05-06 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0002_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='loyalty_1c_code',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='1c code'),
            preserve_default=False,
        ),
    ]