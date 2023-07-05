# syntax=docker/dockerfile:1
FROM python:3.7-alpine

WORKDIR /code

RUN apk add --no-cache gcc musl-dev linux-headers mysql-client git mariadb-dev build-base

# Copy all files except for .env docker-compose.yml and .git
COPY . /code/

# Check if a directory exists and print a message
RUN if [ -d /code/datamodel ]; then \
        echo "Directory 'datamodel' exists"; \
    else \
        echo "Directory 'datamodel' does not exist"; \
    fi

RUN pip install --no-cache-dir .

EXPOSE 5000

CMD ["python", "manage.py", "runserver"]
