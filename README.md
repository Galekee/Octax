# OCTAX — Business Management Platform

Независимый Django-проект для автоматизации малого бизнеса и практики QA.

## Запуск (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

## QA

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

## Важно

Не заменяйте существующую `db.sqlite3` при обновлении. Не публикуйте `.env`, базу данных или `.venv` в GitHub.

Дизайн dashboard и оболочки обновлён. Остальные экраны используют совместимые компоненты; дальнейшая унификация запланирована.
