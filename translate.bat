@echo off
docker run --rm -it ^
  -v %cd%:/app ^
  -w /app ^
  omnipyx-core-image ^
  bash -c "poetry run django-admin makemessages -l es && poetry run django-admin makemessages -l en && poetry run django-admin compilemessages"
