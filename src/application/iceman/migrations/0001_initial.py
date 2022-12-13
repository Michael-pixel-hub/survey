# Generated by Django 2.2.24 on 2022-01-23 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('survey', '0176_task_application'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('order', models.PositiveIntegerField(default=99999999, editable=False)),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
                'db_table': 'iceman_brands',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('order', models.PositiveIntegerField(default=99999999, editable=False)),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
                'db_table': 'iceman_categories',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_created=True, verbose_name='Дата заказа')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='Дата доставки')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='Стоимость заказа')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Комментаорий')),
                ('status', models.IntegerField(choices=[(1, 'Новый'), (2, 'Ждет оплаты'), (3, 'Оплачен'), (4, 'Отмененный')], default=1, verbose_name='Статус')),
                ('payment_type', models.CharField(blank=True, choices=[('online', 'Онлайн'), ('delay', 'Отсрочка 7 дней')], max_length=20, null=True, verbose_name='Тип оплаты')),
                ('payment_status', models.BooleanField(default=False, verbose_name='Оплаченный')),
                ('payment_sum', models.FloatField(blank=True, default=0, verbose_name='Сумма оплаты')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'iceman_orders',
                'ordering': ['-date_create'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('order', models.PositiveIntegerField(default=99999999, editable=False)),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.FileField(blank=True, null=True, upload_to='iceman/products/', verbose_name='Изображение')),
                ('unit', models.CharField(max_length=100, verbose_name='Ед. измерения')),
                ('box_count', models.IntegerField(blank=True, null=True, verbose_name='Кол-во в коробке')),
                ('min_count', models.IntegerField(blank=True, null=True, verbose_name='Минимальное количество')),
                ('is_bonus', models.BooleanField(default=True, verbose_name='Бонусный товар')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Brand', verbose_name='Производитель')),
                ('categories', models.ManyToManyField(to='iceman.Category', verbose_name='Разделы')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'iceman_products',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('sys_name', models.CharField(max_length=255, verbose_name='Системное имя')),
            ],
            options={
                'verbose_name': 'Источник',
                'verbose_name_plural': 'Источники',
                'db_table': 'iceman_sources',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('sys_name', models.CharField(max_length=255, unique=True, verbose_name='Системное имя')),
                ('default', models.BooleanField(default=False, verbose_name='По умолчанию')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iceman_stock_source', to='iceman.Source', verbose_name='Источник')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
                'db_table': 'iceman_stocks',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('code', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Код')),
                ('address', models.TextField(blank=True, max_length=500, verbose_name='Адрес')),
                ('auto_coord', models.BooleanField(default=False, verbose_name='Автоматически определить координаты')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Долгота')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Широта')),
                ('inn', models.CharField(blank=True, default='', max_length=12, verbose_name='ИНН')),
                ('inn_auto', models.BooleanField(default=False, verbose_name='Автоматически загрузить данные')),
                ('inn_name', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='Название организации')),
                ('inn_name_1', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='Полное название организации')),
                ('inn_director_title', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='Должность директора')),
                ('inn_director_name', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='Фио директора')),
                ('inn_address', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='Адрес')),
                ('inn_kpp', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='КПП')),
                ('inn_ogrn', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='ОГРН')),
                ('inn_okved', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='ОКВЭД')),
                ('inn_type', models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='Тип организации')),
                ('is_agreement', models.BooleanField(default=False, verbose_name='Заключен договор')),
                ('lpr_phone', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Телефон продавца')),
                ('lpr_fio', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='ФИО продавца')),
                ('director_phone', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Телефон директора')),
                ('director_fio', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='ФИО директора')),
                ('price_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип цены')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='iceman/stores/photos/', verbose_name='Изображение магазина')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='iceman_store_region', to='survey.Region', verbose_name='Регион')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iceman_store_source', to='iceman.Source', verbose_name='Источник')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'db_table': 'iceman_stores',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='StoreTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sales', models.BooleanField(default=False, verbose_name='Продажа')),
                ('lock_user_id', models.IntegerField(blank=True, null=True, verbose_name='Залочена для пользователя')),
                ('completed', models.BooleanField(default=False, verbose_name='Выполнена')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Store', verbose_name='Магазин')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.Task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Задача в магазине',
                'verbose_name_plural': 'Задачи в магазинах',
                'db_table': 'iceman_stores_tasks',
                'ordering': ['store_id'],
            },
        ),
        migrations.CreateModel(
            name='StoreDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_created=True, verbose_name='Дата загрузки')),
                ('type', models.CharField(choices=[('rent_contract', 'Договор аренды помещения'), ('organization_rule', 'Устав предприятия'), ('director_appointment', 'Назначение ген. директора')], max_length=50, verbose_name='Тип документа')),
                ('number', models.IntegerField(default=1, verbose_name='Страница')),
                ('file', models.ImageField(upload_to='iceman/stores/documents/', verbose_name='Изображение документа')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Store', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Документ магазина',
                'verbose_name_plural': 'Документы магазина',
                'db_table': 'iceman_stores_documents',
                'ordering': ['store_id', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='Остаток')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Product', verbose_name='Товар')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Stock', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Остаток товара на складе',
                'verbose_name_plural': 'Остатки товаров на складе',
                'db_table': 'iceman_products_stocks',
                'ordering': ['product_id', 'stock_id'],
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_type', models.CharField(db_index=True, max_length=255, verbose_name='Тип цены')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Цена товара',
                'verbose_name_plural': 'Цены товара',
                'db_table': 'iceman_products_prices',
                'ordering': ['product_id', 'price_type'],
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('brand_name', models.CharField(max_length=200, verbose_name='Производитель')),
                ('unit', models.CharField(max_length=100, verbose_name='Ед. измерения')),
                ('box_count', models.IntegerField(blank=True, null=True, verbose_name='Кол-во в коробке')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('is_bonus', models.BooleanField(default=False, verbose_name='Бонусный товар')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Order', verbose_name='Заказ')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iceman.Product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
                'db_table': 'iceman_order_products',
                'ordering': ['-order_id', 'id'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iceman_order_source', to='iceman.Source', verbose_name='Источник'),
        ),
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iceman.Store', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='iceman_order_user', to='survey.User', verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Date create')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('message', models.TextField(verbose_name='Message')),
                ('category', models.TextField(choices=[('important', 'Important message'), ('task', 'Task'), ('act', 'Act')], default='important', max_length=20, verbose_name='Category')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Is sent')),
                ('result', models.TextField(blank=True, default='', verbose_name='Result')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='iceman_user', to='survey.User', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'db_table': 'iceman_notifications',
                'ordering': ['-date_create'],
            },
        ),
        migrations.CreateModel(
            name='StoreStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Stock', verbose_name='Склад')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Store', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Склад магазина',
                'verbose_name_plural': 'Склады магазина',
                'db_table': 'iceman_stores_stocks',
                'ordering': ['store_id', 'stock_id'],
                'unique_together': {('store', 'stock')},
            },
        ),
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['address'], name='iceman_stor_address_dbcbe9_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='productstock',
            unique_together={('product', 'stock')},
        ),
        migrations.AlterUniqueTogether(
            name='productprice',
            unique_together={('product', 'price_type')},
        ),
    ]
