from import_export import resources
from import_export.fields import Field

from .models import User, Good, Store


class UserResource(resources.ModelResource):

    id = Field(attribute='id', column_name='Ид')
    date_join = Field(attribute='date_join', column_name='Дата регистрации')
    name = Field(attribute='name', column_name='Имя')
    surname = Field(attribute='surname', column_name='Фамилия')
    phone = Field(attribute='phone', column_name='Телефон')
    email = Field(attribute='email', column_name='E-mail')
    advisor = Field(attribute='advisor', column_name='Менеджер')
    city = Field(attribute='city', column_name='Город')
    status = Field(attribute='status', column_name='Статус Сюрвеер')
    status_agent = Field(attribute='status_agent', column_name='Статус Агент')
    status_iceman = Field(attribute='status_iceman', column_name='Статус Айсмен')
    status_legal = Field(attribute='status_legal', column_name='Юр. статус')
    qlik_status = Field(attribute='qlik_status', column_name='Статус в Клике')
    route = Field(attribute='route', column_name='Название маршрута')
    rank = Field(attribute='rank', column_name='Рейтинг')
    is_fixed_rank = Field(attribute='is_fixed_rank', column_name='Фиксированный рейтинг')
    is_only_self_tasks = Field(attribute='is_only_self_tasks', column_name='Только свои задачи')

    class Meta:
        model = User
        fields = ('id', 'date_join', 'name', 'surname', 'phone', 'email', 'advisor', 'city', 'status', 'status_agent',
                  'status_iceman', 'status_legal', 'qlik_status', 'route', 'rank', 'is_fixed_rank',
                  'is_only_self_tasks')

    def dehydrate_is_only_self_tasks(self, obj):
        return 'Да' if obj.is_only_self_tasks else 'Нет'

    def dehydrate_is_fixed_rank(self, obj):
        return 'Да' if obj.is_fixed_rank else 'Нет'

    def dehydrate_status(self, obj):
        return obj.status.name if obj.status is not None else None

    def dehydrate_status_legal(self, obj):
        return obj.get_status_legal_display()

    def dehydrate_qlik_status(self, obj):
        return obj.get_qlik_status_display()

    def dehydrate_rank(self, obj):
        return obj.rank.name if obj.rank is not None else None


class GoodResource(resources.ModelResource):

    class Meta:
        model = Good
        fields = ('id', 'name', 'code', 'image', 'description')
        export_order = ('id', 'name', 'code', 'image', 'description')

class StoreResource(resources.ModelResource):

    code = Field(attribute='code', column_name='Код клиента')
    factory_code = Field(attribute='factory_code', column_name='Код завода')
    category = Field(attribute='category', column_name='Раздел')
    region_o = Field(attribute='region_o', column_name='Регион')
    client = Field(attribute='client', column_name='Клиент')
    address = Field(attribute='address', column_name='Адрес')
    longitude = Field(attribute='longitude', column_name='Долгота')
    latitude = Field(attribute='latitude', column_name='Широта')
    is_public = Field(attribute='is_public', column_name='Опубликован (да/нет)')
    
    class Meta:
        model = Store
        fields = ('code', 'factory_code', 'category', 'region_o', 'client', 'address', 'longitude', 'latitude',
                  'is_public')

    def dehydrate_is_public(self, obj):
        return 'Да' if obj.is_public else 'Нет'
