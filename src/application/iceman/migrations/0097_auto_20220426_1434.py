# Generated by Django 2.2.24 on 2022-04-26 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0096_order_user_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user_money',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='iceman_order_user_money', to='survey.User', verbose_name='Пользователь получения денег'),
        ),
    ]
