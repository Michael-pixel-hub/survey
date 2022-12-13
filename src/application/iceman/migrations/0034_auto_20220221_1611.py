# Generated by Django 2.2.24 on 2022-02-21 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0033_order_online_payment_qr_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='bonus',
            field=models.FloatField(blank=True, default=20, help_text='На сколько процентов от суммы товаров можно приобрести в качестве бонуса. 0 - нет бонуса.', verbose_name='Бонус в %'),
        ),
        migrations.AddField(
            model_name='source',
            name='delivery_max_days',
            field=models.IntegerField(default=10, help_text='Максимальное число дней доставки', verbose_name='Число дней доставки'),
        ),
        migrations.AddField(
            model_name='source',
            name='discount',
            field=models.FloatField(blank=True, default=5, help_text='Процент скидки при выборе онлайн оплаты. 0 - нет скидки.', verbose_name='Скидка онлайн оплаты в %'),
        ),
        migrations.AddField(
            model_name='source',
            name='email',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='E-mail для получения заказов'),
        ),
        migrations.AddField(
            model_name='source',
            name='sum_restrict',
            field=models.FloatField(blank=True, default=4000, help_text='Ограничение суммы в рублях при . 0 - нет ограничения.', verbose_name='Ограничение суммы в руб.'),
        ),
        migrations.AddField(
            model_name='source',
            name='worker_bonus',
            field=models.FloatField(default=8, help_text='Какой % от стоимости товара выплачивается торговому представителю.', verbose_name='Бонус в % для работника'),
        ),
    ]
