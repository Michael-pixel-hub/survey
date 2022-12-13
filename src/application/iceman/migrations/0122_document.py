# Generated by Django 2.2.28 on 2022-11-15 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0121_auto_20221115_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('sys_name', models.CharField(max_length=255, unique=True, verbose_name='Системное имя')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'db_table': 'iceman_documents',
                'ordering': ['name'],
            },
        ),
    ]
