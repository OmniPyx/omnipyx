# Dockerfile en omnipyx_core

FROM python:3.11-slim

# Seteamos el directorio de trabajo
WORKDIR /app

# Instala herramientas necesarias
RUN apt-get update && \
    apt-get install -y build-essential gettext curl git && \
    pip install --upgrade pip

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copia el core y el módulo local (asegúrate de este orden y contexto)
COPY ./pyproject.toml ./poetry.lock* /app/

# Instala las dependencias
RUN poetry install

# Copia el resto del código core (tu proyecto Django)
COPY . /app/

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
