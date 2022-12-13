# Generated by Django 2.2.24 on 2021-12-29 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0086_tinkoffpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='amount',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='card_id',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Card id'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='error_code',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Error code'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='exp_date',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Exp date'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='order_id',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Order id'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='pan',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Pan'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Payment id'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='status',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='success',
            field=models.BooleanField(blank=True, null=True, verbose_name='Success'),
        ),
        migrations.AlterField(
            model_name='tinkoffpayment',
            name='terminal_key',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Terminal key'),
        ),
    ]
