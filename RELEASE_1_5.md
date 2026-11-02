# OCTAX 1.5 — Leads & Companies

Добавлены самостоятельные разделы **Лиды** и **Компании** с формами, поиском, фильтром статуса лидов и действиями создания, редактирования, удаления. Преобразование лида в клиента создаёт CRM-клиента ровно один раз.

## Установка поверх 1.4

1. Сохраните резервную копию папки и `db.sqlite3`.
2. Скопируйте содержимое папки `octax` из архива в действующий проект, сохранив `.git`, `.venv`, `.env`, `db.sqlite3`.
3. Выполните команды:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py test sales
.\.venv\Scripts\python.exe manage.py runserver
```

4. Откройте `/workspace/leads/` и `/workspace/companies/`.

**QA:** тесты проверяют доступ по владельцу, валидацию привязки компании, одноразовую конвертацию, POST-only и авторизацию. Полный прогон тестов в среде сборки зависит от наличия Django.
