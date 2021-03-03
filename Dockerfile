FROM python:3.9-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev

WORKDIR /usr/local/src/cats_project

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv \
    && pipenv install --system

RUN adduser -D user

USER user

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --chown=user ./ ./

CMD [ "./manage.py", "runserver", "0.0.0.0:8080" ]
