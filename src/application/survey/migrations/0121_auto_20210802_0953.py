# Generated by Django 2.2.24 on 2021-08-02 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0120_taskquestionnairequestion_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskquestionnairequestion',
            name='choices',
            field=models.TextField(blank='', default='', help_text='Enter separated', verbose_name='Choices'),
        ),
    ]
