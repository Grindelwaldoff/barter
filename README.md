# Barter

## Требования

- Python 3.10+
- PostgreSQL 14+ (или совместимая версия)

## Установка и запуск

1. **Клонируйте репозиторий и создайте виртуальное окружение**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

   Конфигурация бд по умолчанию находится в `barter/barter/settings.py` и ожидает параметры подключения:
   - имя БД: `barter`
   - пользователь: `postgres`
   - пароль: `postgres`
   - хост: `localhost`
   - порт: `5432`

   При необходимости можно переключить на sqlite заменив DATABASE на:

    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'barter',
        }
    }
    ```

4. **Примените миграции**
   ```bash
   python manage.py migrate
   ```

5. **Загрузите фикстуры**
   ```bash
   python manage.py loaddata users ads proposals
   ```

   ОБЯЗАТЕЛЬНО ВЫПОЛНИТЬ ПЕРЕД ЗАПУСКОМ
    ```bash
    python manage.py shell -c "from django.contrib.auth import get_user_model as G; U=G(); [ (lambda u: (u.set_password('demo'), u.save()))(U.objects.get(username=f'u{i}')) for i in range(1,9) ] ; print('ok')"
    ```
    Теперь пароль у всех юзеров будет demo

6. **Создайте суперпользователя (опционально)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Запустите локальный сервер**
   ```bash
   python manage.py runserver
   ```

   Приложение будет доступно по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Тесты

Для запуска (из папки репы):

```bash
cd barter && pytest
```

Используется настройка из `pytest.ini` в корне проекта.

## Структура фикстур

- `ads/fixtures/users.json` – пользователи (`u1` … `u8`), без пригодных паролей.
- `ads/fixtures/ads.json` – объявления, связанные с пользователями из фикстуры.
- `ads/fixtures/proposals.json` – предложения обмена между объявлениями.
