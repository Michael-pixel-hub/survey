# Generated by Django 2.2.20 on 2021-05-17 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0011_auto_20210517_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentmenuitem',
            name='action',
            field=models.TextField(choices=[('show_text', 'Show text'), ('debt', 'Receivables')], default='show_text', max_length=20, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='departmentmenuitem',
            name='value',
            field=models.TextField(blank=True, default='', help_text='Formatting telegram message', verbose_name='Description'),
        ),
    ]
