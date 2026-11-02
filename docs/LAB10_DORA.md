# Лабораторная №10 — CI/CD и DORA

## Pipeline
`.github/workflows/ci.yml` запускает проверку синтаксиса, Ruff, Django system check, контроль миграций, миграции SQLite, тесты и проверку зависимостей OSV Scanner; публикует исходники в GitHub Actions artifact. Успех нужно проверить в действительном запуске после push.

## DORA — четыре метрики и источники
1. Deployment frequency — число успешных **production** deployments за период, на основе GitHub Deployments / GitHub Actions release events.
2. Lead time for changes — время от commit до соответствующего production deployment. Связь надо хранить явно.
3. Change failure rate — доля production deployments, вызвавших инцидент, откат или hotfix. Нужен журнал инцидентов.
4. MTTR / failed deployment recovery time — среднее время восстановления после неудачного релиза; нужны timestamps начала/конца инцидента.

Сбор последних CI-запусков реализован через публичный GitHub REST API без токена (rate limit возможен); private repository — задать `GITHUB_TOKEN` в переменной среды локально. Не включайте секрет в исходники. CI runs **не считаются** deployments. Пока реальные сведения о деплоях/инцидентах отсутствуют, дашборд честно показывает «—». Для сдачи следует провести хотя бы учебный production-like deployment с регистрацией timestamp, issue/incident и ссылками и добавить сбор по GitHub API.

## Улучшения
- Сократить время обратной связи PR за счёт автоматического запуска тестов, сравнить длительность с ручной проверкой.
- Добавить лог production deployments и incident timeline, чтобы метрики вычислялись из исходных событий, а не из предположений.

## Защита main
GitHub → Settings → Rules → Rulesets → New ruleset: target `main`, require pull request, 1 reviewer, require status checks `quality`. Для некоторых тарифов и типов репозиториев применение ограничено; проверяйте доступность. Это действие требует прав администратора и не настраивается из локального ZIP.
