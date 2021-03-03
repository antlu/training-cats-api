FROM postgres:12-alpine

ENV POSTGRES_DB=cats_db \
    POSTGRES_USER=dev \
    POSTGRES_PASSWORD=password

COPY --chown=postgres db_init.sql /docker-entrypoint-initdb.d/
