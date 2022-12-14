# Generated by Django 2.2.24 on 2022-03-13 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0061_auto_20220313_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedocument',
            name='type',
            field=models.CharField(choices=[('agreement_card', 'Карточка клиента'), ('agreement_charter', 'Устав предприятия'), ('agreement_director', 'Назначение ген. директора'), ('agreement_photo', 'Договор аренды помещения'), ('document', 'Фото документа')], max_length=50, verbose_name='Тип документа'),
        ),
    ]
