# Vacation API

## Описание
Сервис для отслеживания и модификации отпусков сотрудников.

## Запуск проекта

```bash
git clone https://github.com/Stasyar/Vacations.git

docker compose -f docker-compose.yaml up -d db

docker compose -f docker-compose.yaml up -d --build app
```

### Тесты
```bash
docker compose -f docker-compose-dev.yaml up -d test-db

docker compose -f docker-compose-dev.yaml up -d --build app

docker exec -it <app_container_name> bash

pytest
```
### Линтеры
```bash
docker compose -f docker-compose-dev.yaml up --build

docker exec -it <app_container_name> bash

black . --check 

isort . --check 

flake8 . 
```

## Эндпоинты
### Просмотр последних трех отпусков работника
`GET /vacations/last/{employee_id}`

Пример запроса: `GET /vacations/last/1`
#### Ответ:
```json
[
  {
    "id": 3,
    "employee_id": 1,
    "start_date": "2025-04-01",
    "end_date": "2025-04-07"
  },
]
```
### Создание отпуска
`POST /vacations/`

#### Тело запроса:
```json
{
  "employee_id": 1,
  "start_date": "2025-05-01",
  "end_date": "2025-05-14"
}
```
#### Ответ(200):
```json
{
  "id": 1,
  "employee_id": 1,
  "start_date": "2025-05-01",
  "end_date": "2025-05-14"
}
```

### Просмотр отпуска всех сотрудников за определенный период
`GET /vacation/period`

Пример запроса: `GET /vacations/period?start_date=2025-01-01&end_date=2025-12-31`
#### Ответ:
```json
[
  {
    "id": 2,
    "employee_id": 1,
    "start_date": "2025-06-10",
    "end_date": "2025-06-24"
  },
]

```
### Удаление отауска
`DELETE /vacation/{vacation_id}`

Пример запроса: `DELETE /vacations/1`

#### Ответ(200):
```json
{ "ok": true }
```

#### Ответ (если отпуск не найден):
```json
{
  "detail": "Vacation not found"
}
```


