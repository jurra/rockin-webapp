# syntax=docker/dockerfile:1
FROM python:3.7-alpine

WORKDIR /code

RUN apk add --no-cache gcc musl-dev linux-headers mysql-client git

# Copy all files except for .env docker-compose.yml and .git
COPY datamodel \
    crudapp \
    rockin \
    manage.py \
    setup.py \
    pyproject.toml

RUN pip install .

EXPOSE 5000

CMD ["python", "manage.py", "runserver"]