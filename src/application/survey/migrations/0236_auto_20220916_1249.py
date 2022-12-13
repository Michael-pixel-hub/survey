# Generated by Django 2.2.28 on 2022-09-16 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0235_auto_20220909_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='penalty',
            options={'ordering': ['user'], 'verbose_name': 'Штраф сюрвеера', 'verbose_name_plural': 'Штрафы'},
        ),
        migrations.AlterModelOptions(
            name='penaltyrepayment',
            options={'ordering': ['penalty'], 'verbose_name': 'Погашение штрафа', 'verbose_name_plural': 'Погашение штрафов'},
        ),
        migrations.AlterField(
            model_name='penalty',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='survey_penalty_creator', to='survey.User', verbose_name='Координатор'),
        ),
        migrations.AlterField(
            model_name='penaltyrepayment',
            name='repayment_sum',
            field=models.FloatField(default=0, verbose_name='Сумма погашения'),
        ),
    ]
