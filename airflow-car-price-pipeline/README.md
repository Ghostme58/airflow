# Airflow ML pipeline: car price category prediction

Учебный проект, демонстрирующий оркестрацию ML-пайплайна в Apache Airflow. DAG обучает несколько моделей классификации на данных объявлений о продаже автомобилей, сохраняет лучшую модель и запускает предсказания для JSON-файлов из тестовой выборки.

## Что делает проект

1. DAG `car_price_prediction` по расписанию запускает обучение.
2. В задаче `pipeline` сравниваются `LogisticRegression`, `RandomForestClassifier` и `SVC` с помощью кросс-валидации.
3. Лучшая модель сохраняется в `data/models/`.
4. Задача `predict` применяет последнюю модель к файлам из `data/test/` и создаёт `data/predictions/predictions.csv`.

## Структура

```text
dags/hw_dag.py          # определение Airflow DAG
modules/pipeline.py     # обучение и выбор модели
modules/predict.py      # предсказания
data/train/homework.csv # обучающая выборка
data/test/              # примеры записей для предсказания
docker-compose.yml      # сервисы Airflow, PostgreSQL и Redis
```

Папки `data/models/` и `data/predictions/` намеренно пусты в Git: они заполняются при запуске пайплайна.

## Запуск

Нужны Docker и Docker Compose.

```bash
docker compose up airflow-init
docker compose up -d
```

После запуска откройте [http://localhost:8080](http://localhost:8080). Учётные данные по умолчанию: `airflow` / `airflow`.

В интерфейсе включите DAG `car_price_prediction` и запустите его вручную либо дождитесь расписания: ежедневно в 15:00 UTC.

Для остановки сервисов:

```bash
docker compose down
```

## Примечания

- В проекте отключены стандартные примеры Airflow, поэтому в интерфейсе будет виден только этот DAG.
- Логи, локальные настройки Airflow, модели, предсказания и служебные файлы macOS исключены из Git через `.gitignore`.
- Конфигурация рассчитана на учебный локальный запуск, а не на production-развёртывание.
