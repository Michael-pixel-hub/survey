# Generated by Django 2.2.28 on 2022-09-16 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_show_date_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='show_date_end',
            field=models.BooleanField(default=True, verbose_name='Показывать дату завершения заданий'),
        ),
    ]
