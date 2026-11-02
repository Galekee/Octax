# OCTAX 1.0 — старт

Новая визуальная оболочка существующего Django CRM. Сохранены модели, миграции, URL, существующие QA-тесты и CI.

## Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver
```

Открыть http://127.0.0.1:8000/ . Если команда py не работает, используйте установленный python вместо py.

## GitHub

Рекомендуется создать новый репозиторий `octax` или новую ветку в старом. Перед push убедитесь, что в репозитории нет секретов и клиентских данных.

## Что изменено

Бренд в шаблонах, новая палитра и CSS, светлая тема по умолчанию с сохранением переключателя. Backend и база не переименовывались во избежание поломки миграций.

Это первый этап редизайна, а не готовая новая система. Запуск и тесты в этой среде не подтверждены.
