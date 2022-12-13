# Generated by Django 2.2.28 on 2022-10-07 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0237_auto_20220916_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='application',
            field=models.CharField(choices=[('iceman', 'Айсмен'), ('classic_logistic', 'Классик логистика'), ('classic_logistic_2', '2 Классик логистика'), ('logistic_msk', 'Логистика МСК'), ('logistic_msk_2', '2 Логистика МСК'), ('nefco', 'Нэфис Косметикс'), ('bp_operators', 'Сюрвеер Ш'), ('promotion', 'ГО Айсмен'), ('samberu', 'Самберу'), ('smoroza', 'Смороза Биз'), ('shop_survey', 'Сюрвеер')], default='shop_survey', max_length=20, verbose_name='Проект'),
        ),
        migrations.AlterField(
            model_name='tasksexecution',
            name='application',
            field=models.CharField(choices=[('iceman', 'Айсмен'), ('classic_logistic', 'Классик логистика'), ('classic_logistic_2', '2 Классик логистика'), ('logistic_msk', 'Логистика МСК'), ('logistic_msk_2', '2 Логистика МСК'), ('nefco', 'Нэфис Косметикс'), ('bp_operators', 'Сюрвеер Ш'), ('promotion', 'ГО Айсмен'), ('samberu', 'Самберу'), ('smoroza', 'Смороза Биз'), ('shop_survey', 'Сюрвеер')], default='shop_survey', max_length=20, verbose_name='Проект'),
        ),
    ]
