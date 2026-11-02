# SmartCRM — лабораторные №9 и №10

## Быстрый запуск (PowerShell, Windows 11)
1. Распакуйте ZIP и откройте **папку `smart-crm-system`** в VS Code.
2. В терминале последовательно выполните:

```powershell
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py check
py manage.py test
py manage.py createsuperuser
py manage.py runserver
```

Если `py` не работает, замените `py` на `python` (при установленном Python 3.11+).
Откройте http://127.0.0.1:8000/accounts/login/ и войдите под созданным пользователем.

## ЛЗ 9
В меню «Agile · ЛЗ 9»: создать проект, два спринта, назначить задачи спринтам, двигать задачи между колонками и заполнить ретроспективу. Во вкладке отчёта появятся метрики на основе ваших данных и выгрузка CSV. Инструкция `docs/LAB9_SPRINT_REPORT.md`.

## ЛЗ 10
В меню «CI/CD · ЛЗ 10» будут показаны последние запуски GitHub Actions после публикации workflow. Сам CI: `.github/workflows/ci.yml`. План релиза: `docs/LAB10_RELEASE_PLAN.md`. Требования к DORA: `docs/LAB10_DORA.md`. Внимание: показатели DORA без реальных deployment/incident событий не вычисляются.

## Как обновить GitHub, сохранив историю
**Не удаляйте старый репозиторий.** Сначала клонируйте:
```powershell
git clone https://github.com/szdkvab-maker/smart-crm-system.git
```
Скопируйте **содержимое** папки `smart-crm-system` из этого ZIP внутрь клонированного репозитория с заменой файлов; **не перезаписывайте `.git`**. Затем в папке клона:
```powershell
git status
git add .
git commit -m "Add SmartCRM labs 9 and 10"
git push origin main
```
Если основная ветка называется иначе, используйте её имя. Проверьте GitHub → Actions и ошибки в журнале workflow. Без ваших прав доступа я не могу выполнить push напрямую.

## Что не заявлять преподавателю
- «Два спринта проведены», пока они реально не отработаны.
- «CI зелёный», пока workflow не выполнялся в GitHub.
- «DORA измерена», пока нет deployment/incident событий.

Исходные CRM и финансовые приложения сохранены. Для полноценной сдачи №10 необходимо отдельно пройти Actions в GitHub и собрать реальные deployment/incident события.
