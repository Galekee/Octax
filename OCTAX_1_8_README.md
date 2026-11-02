# OCTAX 1.8

- Рабочие выпадающие фильтры Dashboard: раздел (Обзор бизнеса / Продажи / Задачи) и период (всё время / 7 / 30 / 90 дней).
- Показатели за период вычисляются по дате создания записи. Ближайшие задачи показываются независимо от периода, чтобы не скрывать старые незавершённые задачи.
- GitHub Actions переименован в OCTAX CI; сканер OSV убран из основного quality workflow, поскольку он требовал отдельной настройки и мог ломать сборку независимо от тестов. При необходимости настройте отдельный security workflow.
- Нельзя гарантировать исправление прежнего GitHub failure без доступа к полному логу job.

## Проверка
```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver
```

Перенесите файлы поверх проекта, сохранив `.git`, `.venv`, `.env` и `db.sqlite3`.
