# Generated by Django 2.2.24 on 2022-04-15 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0078_auto_20220415_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='sum_restrict',
            field=models.FloatField(blank=True, default=4000, help_text='Ограничение суммы в рублях при отсрочки. 0 - нет ограничения.', verbose_name='Ограничение суммы в руб.'),
        ),
    ]
