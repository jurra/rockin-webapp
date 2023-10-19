# syntax=docker/dockerfile:1
FROM python:3.8-alpine

WORKDIR /code

RUN apk add --no-cache gcc musl-dev linux-headers mysql-client git mariadb-dev build-base

COPY wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh

# Copy all files except for .env docker-compose.yml and .git
COPY datamodel/ /code/datamodel/
COPY crudapp/ /code/crudapp/
COPY rockin/ /code/rockin/
COPY manage.py setup.py pyproject.toml /code/
COPY pyproject.toml /code/
COPY setup.py /code/
# TODO: Delete this
COPY .env /code/

# this is required for postgres
# RUN apk update && apt-get install -y libpq-dev
# RUN pip install --upgrade pip

RUN pip install .

# EXPOSE 5000

# # CMD ["python", "manage.py", "runserver", "5000:5000"]
