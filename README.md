# YaMDb API [![YaMDb Status](https://github.com/sh2man/yamdb_final/workflows/YaMDb/badge.svg)](https://shields.io/)

API YaMDb - это интерфейс, который позволяет пользователям получать и публиковать отзывы на произведения. 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

## Начало работы

Для запуска проекта на локальной машине в целях разработки и тестирования. See deployment for notes on how to deploy the project on a live system.

### Предварительная подготовка

#### Установка Docker
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop) 
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Установите [Docker Compose](https://docs.docker.com/compose/install/)

### Установка проекта (на примере Linux)

- Создайте папку для проекта YaMDb `mkdir yamdb` и перейдите в нее `cd yamdb`
- Склонируйте этот репозиторий в текущую папку `git clone https://github.com/sh2MAN/infra_sp2 .`.
- Создайте файл `.env` командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:
```sh
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнер в котором будет развернута БД)
DB_PORT=5432 # порт для подключения к БД 
```
- Запустите docker-compose `sudo docker-compose up -d` 
- Примените миграции `sudo docker-compose exec web python manage.py migrate`
- Соберите статику `sudo docker-compose exec web python manage.py collectstatic --no-input`
- Создайте суперпользователя Django `sudo docker-compose exec web python manage.py createsuperuser --email 'admin@yamdb.com'`

## Тестирование и работа API

Для локального тестирования можно загрузить данные из фикстур 
```sh
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
**Подробная документация по API размещена по адресу http://localhost/redoc/.**

### Алгоритм регистрации пользователей

1. Пользователь отправляет запрос с параметром email на `/auth/email/`.
2. Сервис отправляет письмо с кодом подтверждения `(confirmation_code)` на адрес `email`.
3. Пользователь отправляет запрос с параметрами `email` и `confirmation_code` на `/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен)
4. При желании пользователь отправляет PATCH-запрос на `/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли

- **Аноним (не авторизованный пользователь)** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и 
ставить рейтинг произведениям (фильмам/книгам/песням), может комментировать чужие отзывы и ставить им оценки; может 
редактировать и удалять свои отзывы и комментарии.
- **Модератор** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- **Администратор** — полные права на управление проектом и всем его содержимым. Может создавать и удалять категории и 
произведения. Может назначать роли пользователям.
- **Администратор Django** — те же права, что и у роли Администратор.

## В разработке использованы

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Gunicorn](https://gunicorn.org/)
* [Nginx](https://nginx.org/)

## Авторы

* **Sergei Simonov** - [sh2MAN](https://github.com/sh2MAN)
* **Maria Mozgunova** - [MariaMozgunova](https://github.com/MariaMozgunova)
* **Pavel Davidov** - [DavydovPavel](https://github.com/DavydovPavel)

## License [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.md)

This project is licensed under the BSD 3 - see the [LICENSE.md](LICENSE.md) file for details
