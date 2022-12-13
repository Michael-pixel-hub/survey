# Generated by Django 2.2.24 on 2022-05-07 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0203_tasksexecutionoutreason_good'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outreason',
            options={'ordering': ['order'], 'verbose_name': 'Причина отсутствия', 'verbose_name_plural': 'Причины отсутствия'},
        ),
        migrations.AddField(
            model_name='outreason',
            name='order',
            field=models.PositiveIntegerField(default=99999999, editable=False),
        ),
    ]