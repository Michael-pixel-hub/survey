# Shop-survey API

## Users / Пользователи

Эта сущность включает в себя всех пользователей приложения.
Пользователи не зависят от источника: они могут быть добавлены через Telegram, приложение Android, интерфейс администрирования или через API. В любом случае все они попадают в одно хранилище.

**Структура таблицы:**

| Поле | Тип | Обязательно | Запись | Описание |
| - | - | - | - | - |
| id | `integer` | - | - | Внутренний идентификатор записи, заполняется автоматически |
| url | `string` | - | - | Url записи, заполняется автоматически |
| name | `string` | - | да | Реальное имя пользователя, например "Иван" |
| surname | `string` | - | да | Фамилия пользователя, например "Иванов" |
| phone | `string` | - | да | Телефон пользователя в произвольном формате, например "+7 999 1234567" |
| email | `string` | да | да | E-mail пользователя, например "mail@mail.com". Уникальное. |
| city | `string` | - | да | Регион работы пользователя, например "Москва" |
| advisor | `string` | - | да | Рекомендатель в произвольном формате |
| date_join | `string` | - | - | Дата регистрации пользователя, заполняется автоматически |
| is_register | `boolean` | - | да | Маркер того, что пользователь зарегистрирован. Пользователь может быть добавлен в систему, но не зарегистрирован. |
| is_banned | `boolean` | - | да | Маркер того, что пользователь забанен. Забаненные пользователи не должны получать доступ к приложени. |
| longitude | `float` | - | да | Долгота из координат последней точки пребывания пользователя. |
| latitude | `float` | - | да | Широта из координат последней точки пребывания пользователя. |
| source | `string` | да | да | Приложение, из которого зарегистрирован пользователь, например, "Telegram", "Android app" и т.д. |
| api_key | `string` | - | да | Ключ для авторизации пользователя через API. |

> <Badge type="warning">Внимание</Badge> <Badge>Информация</Badge>
>
> При каждой геолокации пользователя желательно обновлять ему поля "longitude" и "latitude". Это позволяет оценить местонахождение пользователя относительно точки выполнения заданий.

### Регистрация пользователя

Метод: `POST`

Адрес: `/<version>/survey/public/user/`

Пример запроса:

```http
POST /v1/survey/public/user/ HTTP/1.1
Content-Type: application/json

{
    "name": "Сергей",
    "surname": "Иванов",
    "phone": "+7 925 1234567",
    "email": "mail@engine2.ru",
    "city": "Москва",
    "advisor": "Рекомендатель",
    "is_register": true,
    "source": "Telegram"
}
```

Пример ответа:

```http
HTTP/1.1 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Location: /v1/survey/public/user/d026fff340634062b438b5444299f23d/
Vary: Accept

{
    "id": 1,
    "url": "/v1/survey/public/user/d026fff340634062b438b5444299f23d/",
    "name": "Сергей",
    "surname": "Иванов",
    "phone": "+7 925 1234567",
    "email": "mail@engine2.ru",
    "city": "Москва",
    "advisor": "Рекомендатель",
    "date_join": "2019-02-19T02:01:35.598211",
    "is_register": true,
    "is_banned": false,
    "longitude": null,
    "latitude": null,
    "source": "Telegram",
    "telegram": {
        "id": null,
        "language_code": null,
        "last_name": null,
        "first_name": null,
        "username": null
    },
    "api_key": "d026fff340634062b438b5444299f23d"
}
```

> <Badge type="warning">Важно</Badge> <Badge>Информация</Badge>
>
> После получения ответа от сервера обязательно сохраните "api_key" созданного пользователя для того чтобы продолжать с ним работать: изменять данные, выполнять задания и т.д.

### Информация о пользователе

Метод: `GET`

Адрес: `/<version>/survey/public/user/<api_key>/`

Пример запроса:
```http
GET /v1/survey/public/user/5bb77d09ee8241689f270575fcc3fe68/ HTTP/1.1
Content-Type: application/json
```
Пример ответа:
```http
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "url": "/v1/survey/public/user/5bb77d09ee8241689f270575fcc3fe68/",
    "name": "Сергей",
    "surname": "Иванов",
    "phone": "+7 (123) 1234567",
    "email": "mail@engine2.ru",
    "city": "Москва",
    "advisor": "Иванов",
    "date_join": "2018-08-13T15:59:21.375224",
    "is_register": true,
    "is_banned": false,
    "longitude": 37.671121,
    "latitude": 55.70665,
    "source": "Telegram",
    "telegram": {
        "id": 240629525,
        "language_code": "ru",
        "last_name": "Rown",
        "first_name": "",
        "username": "mr_rown"
    },
    "api_key": "5bb77d09ee8241689f270575fcc3fe68"
}
```

### Изменение пользователя

Метод: `POST`

Адрес: `/<version>/survey/public/user/<api_key>/`

Пример запроса (в данном случае изменится только 2 поля):

```http
POST /v1/survey/public/user/d026fff340634062b438b5444299f23d/ HTTP/1.1
Content-Type: application/json

{
    "name": "Иван",
    "surname": "Петров"
}
```



Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "url": "/v1/survey/public/user/d026fff340634062b438b5444299f23d/",
    "name": "Иван",
    "surname": "Петров",
    "phone": "+7 925 1234567",
    "email": "mail@engine2.ru",
    "city": "Москва",
    "advisor": "Рекомендатель",
    "date_join": "2019-02-19T02:01:35.598211",
    "is_register": true,
    "is_banned": false,
    "longitude": null,
    "latitude": null,
    "source": "Telegram",
    "telegram": {
        "id": null,
        "language_code": null,
        "last_name": null,
        "first_name": null,
        "username": null
    },
    "api_key": "d026fff340634062b438b5444299f23d"
}
```

## Clients / Сети магазинов (клиенты)

Эта сущность включает в себя торговые сети. Например "Пятерочка" или "Магнит". Каждый магазин, заведенный в приложении, принадлежит к торговой сети.

**Структура таблицы:**

| Поле | Тип | Обязательно | Запись | Описание |
| - | - | - | - | - |
| id | `integer` | - | - | Внутренний идентификатор записи, заполняется автоматически |
| url | `string` | - | - | Url записи, заполняется автоматически |
| name | `string` | - | да | Название клиента, например "Пятерочка" |


### Список клиентов

Метод: `GET`

Адрес: `/<version>/survey/public/clients/`

Пример запроса:
```http
GET /v1/survey/public/clients/ HTTP/1.1
Content-Type: application/json
```
Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 841,
    "next": "/v1/survey/public/clients/?page=2",
    "previous": null,
    "results": [
        {
            "id": 220,
            "url": "/v1/survey/clients/220/",
            "name": "5 шагов **"
        },
        {
            "id": 509,
            "url": "/v1/survey/clients/509/",
            "name": "7Я Семья МСК"
        },
        {
            "id": 18,
            "url": "/v1/survey/clients/18/",
            "name": "7Я Семья СЗФ"
        },
        {
            "id": 768,
            "url": "/v1/survey/clients/768/",
            "name": "EUROSPAR"
        },
        <...>
    ]
}
```

Список разбит на страницы по 10 записей на каждой и отсортирован по названию.
Для того, чтобы получить следующую страницу, используйте поле `next` или `previous` в полученном ответе.

### Поиск клиента


Метод: `GET`

Адрес: `/<version>/survey/public/clients/search/<query>/`

Пример запроса:
```http
GET /v1/survey/public/clients/search/Магнит/ HTTP/1.1
Content-Type: application/json
```

Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 247,
            "url": "/v1/survey/clients/247/",
            "name": "Магна ** Морская наб. д.15"
        },
        {
            "id": 30,
            "url": "/v1/survey/clients/30/",
            "name": "Магна ** Морская наб. д.9+ 2 холодильника ЧЛ,ИНМ"
        },
        {
            "id": 755,
            "url": "/v1/survey/clients/755/",
            "name": "Магнит"
        },
        {
            "id": 750,
            "url": "/v1/survey/clients/750/",
            "name": "Магнит ММ"
        },
        <...>
    ]
}

```

Список разбит на страницы по 10 записей на каждой и отсортирован по названию.
Для того, чтобы получить следующую страницу, используйте поле `next` или `previous` в полученном ответе.


### Информация о клиенте

Метод: `GET`

Адрес: `/<version>/survey/public/clients/<id>/`

Пример запроса:
```http
GET /v1/survey/public/clients/1/ HTTP/1.1
Content-Type: application/json
```

Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "url": "/v1/survey/clients/1/",
    "name": "Дикси П"
}
```

Если клиент с указанным `id` не существует, то сервер отдаст код ответа `404`.


## Categories / Группы магазинов

Эта сущность включает в группы магазинов. Например "Локальные Сети" или "Федеральные сети". Каждый магазин, заведенный в приложении, принадлежит к одной из групп.

**Структура таблицы:**

| Поле | Тип | Обязательно | Запись | Описание |
| - | - | - | - | - |
| id | `integer` | - | - | Внутренний идентификатор записи, заполняется автоматически |
| url | `string` | - | - | Url записи, заполняется автоматически |
| name | `string` | - | да | Название группы, например "Локальные Сети" |


### Список групп

Метод: `GET`

Адрес: `/<version>/survey/public/categories/`

Пример запроса:
```http
GET /v1/survey/public/categories/ HTTP/1.1
Content-Type: application/json
```
Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "url": "/v1/survey/public/categories/1/",
            "name": "Федеральные сети"
        }
        <...>
    ]
}
```

Список разбит на страницы по 10 записей на каждой и отсортирован по названию.
Для того, чтобы получить следующую страницу, используйте поле `next` или `previous` в полученном ответе.

### Поиск группы


Метод: `GET`

Адрес: `/<version>/survey/public/categories/search/<query>/`

Пример запроса:
```http
GET /v1/survey/public/categories/search/сети/ HTTP/1.1
Content-Type: application/json
```

Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "url": "/v1/survey/public/categories/1/",
            "name": "Федеральные сети"
        }
        <...>
    ]
}

```

Список разбит на страницы по 10 записей на каждой и отсортирован по названию.
Для того, чтобы получить следующую страницу, используйте поле `next` или `previous` в полученном ответе.


### Информация о группе магазинов

Метод: `GET`

Адрес: `/<version>/survey/public/categories/<id>/`

Пример запроса:
```http
GET /v1/survey/public/categories/1/ HTTP/1.1
Content-Type: application/json
```

Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "url": "/v1/survey/public/categories/1/",
    "name": "Федеральные сети"
}
```

Если группа магазинова с указанным `id` не существует, то сервер отдаст код ответа `404`.

## Regions / Регионы

Эта сущность включает в себя регионы, в которых работают магазины. Например "Москва" или "Ленинградская область". Каждый магазин, заведенный в приложении, принадлежит к региону.

**Структура таблицы:**

| Поле | Тип | Обязательно | Запись | Описание |
| - | - | - | - | - |
| id | `integer` | - | - | Внутренний идентификатор записи, заполняется автоматически |
| url | `string` | - | - | Url записи, заполняется автоматически |
| name | `string` | - | да | Название региона, например "Москва" |


### Список регионов

Метод: `GET`

Адрес: `/<version>/survey/public/regions/`

Пример запроса:
```http
GET /v1/survey/public/regions/ HTTP/1.1
Content-Type: application/json
```
Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 161,
    "next": "/v1/survey/public/regions/?page=2",
    "previous": null,
    "results": [
        {
            "id": 92,
            "url": "/v1/survey/public/regions/92/",
            "name": "Адыгея Респ"
        },
        {
            "id": 121,
            "url": "/v1/survey/public/regions/121/",
            "name": "Алтайский край"
        },
        {
            "id": 83,
            "url": "/v1/survey/public/regions/83/",
            "name": "Архангельская обл"
        },
        <..>
    ]
}
```

Список разбит на страницы по 10 записей на каждой и отсортирован по названию.
Для того, чтобы получить следующую страницу, используйте поле `next` или `previous` в полученном ответе.

### Поиск региона


Метод: `GET`

Адрес: `/<version>/survey/public/regions/search/<query>/`

Пример запроса:
```http
GET /v1/survey/public/regions/search/Москва/ HTTP/1.1
Content-Type: application/json
```

Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "url": "/v1/survey/public/regions/5/",
            "name": "Москва"
        },
        <..>
    ]
}
```

Список разбит на страницы по 10 записей на каждой и отсортирован по названию.
Для того, чтобы получить следующую страницу, используйте поле `next` или `previous` в полученном ответе.

### Информация о регионе

Метод: `GET`

Адрес: `/<version>/survey/public/regions/<id>/`

Пример запроса:
```http
GET /v1/survey/public/regions/1/ HTTP/1.1
Content-Type: application/json
```

Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "url": /v1/survey/public/regions/1/",
    "name": "Санкт-Петербург г"
}
```

Если регион с указанным `id` не существует, то сервер отдаст код ответа `404`.

## Stores / Магазины

Эта сущность включает в себя магазины, в которых пользователи могут выполнять задания. Магазины можно искать по координатам.

**Структура таблицы:**

| Поле | Тип | Обязательно | Запись | Описание |
| - | - | - | - | - |
| id | `integer` | - | - | Внутренний идентификатор записи, заполняется автоматически |
| url | `string` | - | - | Url записи, заполняется автоматически |
| code | `string` | - | да | Внутренний код магазина |
| address | `string` | - | да | Физический адрес магазина |
| longitude | `float` | - | да | Долгота координат физического расположения магазина |
| latitude | `float` | - | да | Широта координат физического расположения магазина |
| client | `data` | да | - | Сеть магазинов, к которой принадлежит этот магазин |
| [client]&nbsp;id | `integer` | - | - | Идентификатор сети магазинов |
| [client]&nbsp;name | `string` | - | - | Название сети магазинов |
| [client]&nbsp;url | `string` | - | - | Ссылка на объект сети магазинов |
| category | `data` | - | - | Группа магазинов, к которой принадлежит этот магазин |
| [category]&nbsp;id | `integer` | - | - | Идентификатор группы магазинов |
| [category]&nbsp;name | `string` | - | - | Название группы магазинов |
| [category]&nbsp;url | `string` | - | - | Ссылка на объект группы магазинов |
| region | `data` | - | - | Регион, в котором находится этот магазин |
| [region]&nbsp;id | `integer` | - | - | Идентификатор региона |
| [region]&nbsp;name | `string` | - | - | Название региона |
| [region]&nbsp;url | `string` | - | - | Ссылка на объект региона |
| distance | `float` | - | - | Расстояние до магазина, отображается только в поиске по координатам, в километрах |


### Список магазинов

Метод: `GET`

Адрес: `/<version>/survey/public/stores/`

Пример запроса:
```http
GET /v1/survey/public/stores/ HTTP/1.1
Content-Type: application/json
```
Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 10908,
    "next": "/v1/survey/public/stores/?page=2",
    "previous": null,
    "results": [
        {
            "id": 610,
            "url": "/v1/survey/public/stores/610/",
            "code": "СПБС6058",
            "address": "г.СПб., ул.Тельмана, д.40",
            "longitude": 30.478652,
            "latitude": 59.893746,
            "client": {
                "id": 220,
                "name": "5 шагов **",
                "url": "/v1/survey/public/clients/220/"
            },
            "category": {
                "id": null,
                "name": null,
                "url": null
            },
            "region": {
                "id": 1,
                "name": "Санкт-Петербург г",
                "url": "/v1/survey/public/regions/1/"
            },
            "distance": null
        },
        {
            "id": 2274,
            "url": "/v1/survey/public/stores/2274/",
            "code": "СПБУ2705",
            "address": "г.Санкт-Петербург, пр.Шлиссельбургский, д.14",
            "longitude": 30.498208,
            "latitude": 59.839579,
            "client": {
                "id": 220,
                "name": "5 шагов **",
                "url": "/v1/survey/public/clients/220/"
            },
            "category": {
                "id": null,
                "name": null,
                "url": null
            },
            "region": {
                "id": 1,
                "name": "Санкт-Петербург г",
                "url": "/v1/survey/public/regions/1/"
            },
            "distance": null
        },
        {
            "id": 3257,
            "url": "/v1/survey/public/stores/3257/",
            "code": "СПБТ9071",
            "address": "Москва г., Волоколамское шоссе, д.13",
            "longitude": 37.495716,
            "latitude": 55.808078,
            "client": {
                "id": 509,
                "name": "7Я Семья МСК",
                "url": "/v1/survey/public/clients/509/"
            },
            "category": {
                "id": 1,
                "name": "Федеральные сети",
                "url": "/v1/survey/public/categories/1/"
            },
            "region": {
                "id": 79,
                "name": "Москва г",
                "url": "/v1/survey/public/regions/79/"
            },
            "distance": null
        },
        <..>
    ]
}
```

Список разбит на страницы по 10 записей на каждой и отсортирован по сети, а потом коду.
Для того, чтобы получить следующую страницу, используйте поле `next` или `previous` в полученном ответе.

### Информация о магазине

Метод: `GET`

Адрес: `/<version>/survey/public/stores/<id>/`

Пример запроса:
```http
GET /v1/survey/public/stores/3257/ HTTP/1.1
Content-Type: application/json
```

Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 3257,
    "url": "/v1/survey/public/stores/3257/",
    "code": "СПБТ9071",
    "address": "Москва г., Волоколамское шоссе, д.13",
    "longitude": 37.495716,
    "latitude": 55.808078,
    "client": {
        "id": 509,
        "name": "7Я Семья МСК",
        "url": "/v1/survey/public/clients/509/"
    },
    "category": {
        "id": 1,
        "name": "Федеральные сети",
        "url": "/v1/survey/public/categories/1/"
    },
    "region": {
        "id": 79,
        "name": "Москва г",
        "url": "/v1/survey/public/regions/79/"
    },
    "distance": null
}
```

Если магазин с указанным `id` не существует, то сервер отдаст код ответа `404`.


### Поиск магазина по координатам


Метод: `GET`

Адрес: `/<version>/survey/public/stores/geo/<longitude>:<latitude>/`

Пример запроса:
```http
GET /v1/survey/public/stores/geo/37.620952:55.755691/ HTTP/1.1
Content-Type: application/json
```

Пример ответа:

```http
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 602,
    "next": "/v1/survey/public/stores/geo/37.620952:55.755691/?page=2",
    "previous": null,
    "results": [
        {
            "id": 3392,
            "url": "h/v1/survey/public/stores/3392/",
            "code": "МСК004391",
            "address": "119330, г.Москва, Мичуринский пр-кт Олимпийская деревня, д.4/3",
            "longitude": 37.617635,
            "latitude": 55.755814,
            "client": {
                "id": 748,
                "name": "Билла",
                "url": "/v1/survey/public/clients/748/"
            },
            "category": {
                "id": null,
                "name": null,
                "url": null
            },
            "region": {
                "id": 79,
                "name": "Москва г",
                "url": "/v1/survey/public/regions/79/"
            },
            "distance": 0.20870990877
        },
        {
            "id": 9496,
            "url": "/v1/survey/public/stores/9496/",
            "code": "00-00002043",
            "address": "121596,,Москва,М Неделина-4",
            "longitude": 37.617635,
            "latitude": 55.755814,
            "client": {
                "id": 754,
                "name": "Пятерочка",
                "url": "/v1/survey/public/clients/754/"
            },
            "category": {
                "id": null,
                "name": null,
                "url": null
            },
            "region": {
                "id": 133,
                "name": "-",
                "url": "/v1/survey/public/regions/133/"
            },
            "distance": 0.20870990877
        },
        <..>
    ]
}
```

Список разбит на страницы по 10 записей на каждой и отсортирован по расстоянию.
Для того, чтобы получить следующую страницу, используйте поле `next` или `previous` в полученном ответе.
