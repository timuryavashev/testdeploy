# Указываем базовый образ
FROM python:3.14

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# RUN apt-get update \
#   && apt-get install -y gcc libpg-dev \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install --upgrade poetry

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./

# Отключаем создание отдельного venv
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости проекта
RUN poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

RUN mkdir -p /app/media

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]