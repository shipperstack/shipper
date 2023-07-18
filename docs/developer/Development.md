# Development

## Coding standards

- Linting: `flake8` + `mccabe`
- Formatting: `black`

## Setting up a development environment

There are two ways of setting up a development environment.

### Set up with Docker (recommended)

Use the files within the `docker/` directory.

If you need help, run the following commands within the directory:

```
source activate
helpme
```


### Set up manually

In this method you need to bring your own database, or use the built-in SQLite database. A web server (nginx) may also be installed alongside, but it is not necessary if you wish to just use Django's built-in web server.

A manual setup provides easy code reload, since changes will propagate immediately.

#### Prepare the `.env` file

Create an `.env` file by [following the configuration instructions](../sysadmin/Configuration.md).

Be sure to clear out the database portion if you are using the built-in SQLite database.

#### Import the `.env` file

On macOS and Linux, run the following command:

```bash
set -a && source .env && set +a
```

On Windows, this command will not work. If you know of a command that will ingest environment variables from an `.env` file on Windows, please create a patch and make a pull request.

#### Start the development server

Run:

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

#### Caveats

Any tasks that rely on Celery to run will not work. You can try and run Celery separately using the following step, but at that point this method is not recommended, and it's best if you go with a Docker development setup directly.

#### Get Celery tasks to work

Install RabbitMQ.

After installing, run the following commands, with each command going in a different TTY as they will not fork:

```bash
celery -A core worker -l info -Q default
celery -A core worker -l info -Q mirror_upload --concurrency=1
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```