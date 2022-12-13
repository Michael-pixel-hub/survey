# Generated by Django 2.2.24 on 2022-03-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0059_region_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedocument',
            name='type',
            field=models.CharField(choices=[('agreement_card', 'Карточка клиента'), ('agreement_charter', 'Устав предприятия'), ('agreement_director', 'Назначение ген. директора'), ('agreement_photo', 'Договор аренды помещения'), ('document', 'Документ')], max_length=50, verbose_name='Тип документа'),
        ),
    ]