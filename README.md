# Проект AzbukaMebeli

Проект направлени на получение информации с сайта и анализ данных с сайта azbykamebeli.ru. 
  
## Основные задачи:
1) Получеие информации о товарах с сайта azbykamebeli.ru (модуль parse.py)

2) Отпаравка информации в базу данных (пакет data_base)

3) Анализ полученных данных и составление графиков. (analitics.pbix)

## Основной стек технологий:

### aiohtttp
Для быстрого и асинхронного сбора информации с сайта.

### SQLAlchemy
Для организации связей с базой данных. Работа с базой данных с помощью объектно-ориентированного кода, не используя SQL-запросы.
SQLAlchemy позволяет быстро мигрировать с одной базы данных на другую не переписывая код.

### PostgresSQL
База данных с открытым исходным кодом. На выбор базы данных повлияло использования именно этой базы данных в компании "Империя Мебели".

### Docker
Платформа контейнеризации с открытым исходным кодом. Используется для создания образа базы данных PostgresSQL и развертывания приложения на сервере.

### Power BI
Удобный и мощный механизм для визуализации данных.

### Poetry
Современный менеджер пакетов для Python.

## Структура проекта

- docker-compose.yml  - конфигурационный файл в YAML-формате, описывающий логику запуска базы данных PostgresSQL.
- main.py - запускает программу получения информации с сайта azbykamebeli.ru (нужной категории) и добавления информации в базу данных
- parse.py - модуль с логикой скрапинга и парсинга информации с с сайта azbykamebeli.ru (нужной категории)
- data_base - слой работы с базой данных
- analitics.pbix - аналитика и визуализация данных в Power BI
- analitics.pdf - итоговые графики и диаграммы

## Политика работы с конфидициальными данными

В конфигурационных файлах и файлах программы не указаны логины и пароли для подключнния к базе данных. Название, логин и пароль к базе данных должны задаваться в переменных окружения:
$Env:postgres_db
$Env:pguser
$Env:pgpassword 