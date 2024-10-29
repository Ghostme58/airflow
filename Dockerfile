FROM apache/airflow:2.10.2

USER root
# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow
# Обновление pip и setuptools
RUN pip install --upgrade pip setuptools --disable-pip-version-check
# Копирование файла с зависимостями
COPY requirements.txt /requirements.txt
# Установка зависимостей из requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt