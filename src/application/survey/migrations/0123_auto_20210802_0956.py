# Generated by Django 2.2.24 on 2021-08-02 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0122_auto_20210802_0954'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taskquestionnairequestion',
            unique_together={('name', 'questionnaire')},
        ),
    ]
