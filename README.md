## Как установить
Клонировать репозиторий
```git clone https://github.com/kerplunk1/minstroy_parcer.git```
Перейти в клонированный репозиторий
```cd minstroy_parcer```
Создать виртуальное окружение для установки пакетов
```python -m venv venv```
Активировать виртуальное окружение
```.\venv\Scripts\activate```
Установить необходимые пакеты
```pip install -r requirements.txt```

## Как работать
Если виртуальное окружение не активировано, активировать
```.\venv\Scripts\activate``` - для windows, 
либо ```source venv/bin/activate``` - для linux

Отредактировать файл .db_credentials, ввести информацию для подключения к базе данных,
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

