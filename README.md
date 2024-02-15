# Django PostgresML example

## Setup

This example application requires a PostgreSQL database with the PostgresML and pgvector extensions installed. The easiest way to get one is to sign up
for a free database on [postgresml.org](https://postgresml.org).


### Setting `DATABASE_URL`

In your shell, export the `DATABASE_URL` variable with the connection string to your database. For example:

```bash
export DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/postgres
```

### Running the app

```bash
./manage.py migrate
./manage.py runserver
```
