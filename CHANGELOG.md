## 1.5 — Leads & Companies
- Новые модели, миграция, формы, страницы и QA-тесты.
- Добавлена конвертация лида в клиента.

# Changelog

## 4.0 — Dashboard rebuild
- Переработаны главная страница, боковое меню, логотип и дизайн-система.
- Убраны старые лабораторные документы, кэш, локальная база, окружение и история Git из архива.
- Сохранены Django-приложения, маршруты, миграции и тесты.
- Нулевые показатели показывают реальные пустые состояния; фиктивные продажи не добавлены.

### Ограничения
Полный браузерный регресс и тестирование в среде пользователя не проводились.

## 1.6 — QA demo data
- Added `seed_demo` and `clear_demo` commands with user/batch scoping and safety checks.
- Added regression tests for creation, preview, cleanup and duplicate prevention.
- See `DEMO_DATA.md` for usage.
