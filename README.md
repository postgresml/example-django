# Django PostgresML example

## Setup

This example application requires a PostgreSQL database with the PostgresML and pgvector extensions installed. The easiest way to get one is to sign up
for a free database on [postgresml.org](https://postgresml.org).

We're using `curl` to make requests to the app, so if you don't have it already install both `curl` and `jq`.

### Virtualenv

It's recommended to use a virtual environment to run this example. You can create one using the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

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

## Usage

### Adding a TODO item

Using cURL, make a POST request to `/api/todo/` with the two required fields, description & due date:

```bash
curl \
    --silent \
    -X POST \
    -d '{"description": "Make a New Year resolution list", "due_date": "2025-01-01"}' \
    -H 'Content-Type: application/json' \
    http://localhost:8000/api/todo/
```

### Searching for similar items

```bash
curl \
    --silent \
    -H "Content-Type: application/json" \
    'http://localhost:8000/api/todo/search/?q=resolution&limit=1' | jq ".[0].description"
```
