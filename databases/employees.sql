-- Таблицы сохраняем в плоском формате без сложных связей
-- Включаем поддержку внешних ключей
PRAGMA foreign_keys = ON;

-- 1. Сотрудники (каталог + аутентификация)
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date TEXT NOT NULL, -- ISO8601: 'YYYY-MM-DD'
    position TEXT NOT NULL,
    department TEXT, -- Простой текст вместо отдельной таблицы
    skills TEXT, -- Навыки через запятую
    interests TEXT, -- Интересы через запятую
    email TEXT UNIQUE,
    password_hash TEXT, -- Для авторизации
    role TEXT DEFAULT 'user' -- Простые роли: admin/user
);

-- 2. Мероприятия (календарь)
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_time TEXT NOT NULL, -- ISO8601: 'YYYY-MM-DD HH:MM'
    end_time TEXT NOT NULL,
    type TEXT CHECK(type IN ('meeting', 'birthday', 'other')),
    organizer_id INTEGER REFERENCES employees(id) ON DELETE SET NULL
);

-- 3. Участники мероприятий
CREATE TABLE event_participants (
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'invited',
    PRIMARY KEY (event_id, employee_id)
);

-- 4. Расписание занятости (для рекомендаций)
CREATE TABLE schedule (
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    PRIMARY KEY (employee_id, start_time)
);

-- Индексы для быстрого поиска
CREATE INDEX idx_employees_name ON employees(first_name, last_name);
CREATE INDEX idx_events_time ON events(start_time);
CREATE INDEX idx_schedule ON schedule(employee_id, start_time);
