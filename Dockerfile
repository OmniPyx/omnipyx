# Dockerfile para Omnipyx Core con gettext y Poetry
FROM python:3.11-slim

# Set env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear directorios
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y build-essential gettext curl git && \
    pip install --upgrade pip

# Instalar Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copiar archivos de proyecto
COPY pyproject.toml poetry.lock* /app/

# Instalar dependencias del proyecto
RUN poetry install --no-root

# Copiar el resto del código
COPY . /app/

# Crear volumen para la persistencia de traducciones y otros assets
VOLUME ["/app/locale"]

# Puerto por defecto
EXPOSE 8000

# Comando por defecto
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
