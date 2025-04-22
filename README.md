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

- `GET /vacations/last/{employee_id}` — посмотреть последние три отпуска работника
- `POST /vacations/` — создать отпуск
- `GET /vacation/period` — посмотреть отпуска всех сотрудников за определенный период
- `DELETE /vacation/{vacation_id}` — удалить отпуск

