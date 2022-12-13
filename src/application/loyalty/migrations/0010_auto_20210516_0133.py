# Generated by Django 2.2.20 on 2021-05-16 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0009_auto_20210516_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentmenuitem',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterUniqueTogether(
            name='departmentmenuitem',
            unique_together={('department', 'name')},
        ),
    ]
