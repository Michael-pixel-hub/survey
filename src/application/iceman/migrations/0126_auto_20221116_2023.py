# Generated by Django 2.2.28 on 2022-11-16 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0125_documentgroup_documentgroupdocument'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='documentgroupdocument',
            unique_together={('document', 'group')},
        ),
    ]
