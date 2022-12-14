# Generated by Django 2.1 on 2019-11-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspector', '0004_manufacturer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Name')),
                ('internal_id', models.IntegerField(unique=True, verbose_name='Internal id')),
                ('date_update', models.DateTimeField(auto_now_add=True, verbose_name='Date update')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
                'db_table': 'inspector_brands',
                'ordering': ['name'],
            },
        ),
    ]
