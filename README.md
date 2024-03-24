## Как установить
Клонировать репозиторий
```git clone https://github.com/kerplunk1/minstroy_parcer.git```

Перейти в клонированный репозиторий
```cd minstroy_parcer```

Создать виртуальное окружение для установки пакетов
```python -m venv venv```

Активировать виртуальное окружение
```.\venv\Scripts\activate``` - для windows,
либо ```source venv/bin/activate``` - для linux

Установить необходимые пакеты
```pip install -r requirements.txt```

Отредактировать файл .db_credentials, ввести информацию для подключения к базе данных.

Инициализировать alembic для миграций
```alembic init alembic```

Заменить файл alembic\env.py на готовый
```cp env.py alembic\env.py```

Создать начальную ревизию базы данных
```alembic revision --autogenerate -m "init revision"```
> [!IMPORTANT]
> Перед началом миграции убедитесь что в текущей базе данных нет таблиц, т.к. alembic их удалит.

Запустить миграции
```alembic upgrade head```

## Как работать
### Запустить скрипт get_urls.py для сбора ссылок. 
```python get_urls.py```

Первый запуск может быть немного долгим, т.к. селениум сначала установит нужные для него зависимости, веб-драйвер и т.п. Остальные запуски будут побыстрее.
Затем селениум сам отфильтрует нужных поставщиков и начнет сбор ссылок на них.

### Запустить скрипт get_suppliers.py для сбора информации по поставщикам.
```python get_suppliers.py```

Селениум начнет открывать по очереди все ранее собранные ссылки (за текущую дату) и собирать информацию о каждом поставщике.

## Исключения
> [!IMPORTANT]
> Парсер работает довольно стабильно, но все-таки иногда бывают непредвиденные ошибки из-за того что на странице у какого-либо поставшика может отсутствовать какая-либо информация,
> Селениум не может найти какой-либо HTML элемент, либо этот элемент "некликабельный", страница не смогла загрузиться по таймауту и т.п.
> На данный момент обработка таких исключений сводится к пропуску страниц где они произошли.
>
> Если все-таки произошла непредвиденная ошибка из-за которой выполнение скрипта остановилось, чтобы не начинать сначала, в самом скрипте get_suppliers.py есть закоммеентированая строчка
> ![image](https://github.com/kerplunk1/minstroy_parcer/assets/110846988/243a4dde-bb4e-447a-9512-16645259b998)
> можно попробовать начать с последней успешной страницы, расскомментировав эту строку и изменив "Urls.id > 292", закомментировав строчку выше, где фильтрация идет только по дате - продолжить парсинг с ссылки чей id больше последней успешной.
>
> Чтобы исключить подобные ошибки рекомендуется использовать стабильный интернет, запускать скрипт ночью, чтобы не было сильной нагрузки на базу данных сайта, отключить переход компьютера в сон и т.п.
> По времени на каждую страницу уходит примерно 5-10 секунд в среднем, страниц обычно бывает больше 7 тыс.
> 
