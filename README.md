#  Django сборщик анкет + api
#### Проект для реализации сбора анкет и обработки форм
Стэк:
**Django+DRF+Bootstrap**

## Основные функции:
* Добавление данных из формы
* Просмотр всех сообщений
* Фильтры поиска в REST API
* CBV
* Шаблоны, Bootstrap
* Страница регистрации и логина
* DRF REST API
* Github Auth
* Unit тесты
* Swagger

## Как запустить
1. python3 manage.py collectstatic
2. python3 manage.py runserver

## Главная
![img](FORM_MSG/IMAGES_FOR_README/index.png)

## Страница с комментариями
![img](FORM_MSG/IMAGES_FOR_README/by_id.png)

## Страница входа
## http://127.0.0.1:8000/signup/
![img](FORM_MSG/IMAGES_FOR_README/Снимок%20экрана%202022-11-21%20140935.png)

## Страница пользователя
![img](FORM_MSG/IMAGES_FOR_README/Снимок%20экрана%202022-11-14%20010653.png)

## Форма редактирования
![img](FORM_MSG/IMAGES_FOR_README/Снимок%20экрана%202022-11-14%20010721.png)

## DRF endpoints
### http://127.0.0.1:8000/api/v1/msg/
### http://127.0.0.1:8000/api/v1/users_vset
### http://127.0.0.1:8000/api/v1/users_vset/1/

## Swagger 
### http://127.0.0.1:8000/api/v1/swagger
![img](FORM_MSG/IMAGES_FOR_README/Снимок%20экрана%202022-11-14%20005110.png)
