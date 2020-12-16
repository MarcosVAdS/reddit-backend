# Reddit-backend

## Instructions to Run

- Create the virtual environment and activate it

```
virtualenv -p python3 venv
source venv/bin/activate
```

- Install the requirements `pip install -r requirements.txt`

- Start the dockers (`docker-compose up`) with the database and the localstack

- Apply the migrations: `python manage.py migrate`

- Create a super user: `python manage.py createsuperuser`

- Run the server with `python manage.py runserver 8000`

- You need a `.env` file with your environment variables, here's an example file:

  - The `SECRET_KEY` can be generated with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`

```
LOAD_ENVS_FROM_FILE='True'
ENVIRONMENT='development'
SECRET_KEY='#*=backend-challenge=*#'
DEFAULT_FROM_EMAIL='Challenge <challenge@jungledevs.com>'
DATABASE_URL='postgres://postgres:postgres@localhost:5433/boilerplate'
SENTRY_DSN='sentry_key'
AWS_STORAGE_BUCKET_NAME='reddit-backend-django-be'
```

## How to explore

There are some ways to explore the API.

- Accessing the Admin application (`http://localhost:8000/admin`) endpoint to manage the entities.

- Using the Swagger form (`http://localhost:8000/`) to test all the endpoints and understand their behavior.

- Visiting and testing the all the endpoints, one-by-one (`http://localhost:8000/api/v1/*`).

- Reading and running the unit tests (`./manage.py test`).
