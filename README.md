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

### Searching for similar TODO items

```bash
curl \
	--silent \
	-H "Content-Type: application/json" \
	'http://localhost:8000/api/todo/search/?q=resolution&limit=1' | jq ".[0].description"
```
