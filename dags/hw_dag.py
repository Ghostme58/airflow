import datetime as dt
import os
import sys
from airflow.models import DAG
from airflow.operators.python import PythonOperator

# Укажите путь к проекту
path = '/opt/airflow'
# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции
sys.path.insert(0, path)

from modules.pipeline import pipeline
from modules.predict import predict  # Импорт функции предсказания

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(
        dag_id='car_price_prediction',
        schedule="00 15 * * *",
        default_args=args,
        catchup=False  # Не выполнять пропущенные DAG'и
) as dag:
    
    # Задача: запуск пайплайна
    pipeline_task = PythonOperator(
        task_id='pipeline',
        python_callable=pipeline,
        dag=dag,
    )

    # Задача: предсказание
    predict_task = PythonOperator(
        task_id='predict',
        python_callable=predict,
        dag=dag,
    )

    # Определяем порядок выполнения задач
    pipeline_task >> predict_task