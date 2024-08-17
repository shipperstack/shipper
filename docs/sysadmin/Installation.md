# Installation

## Requirements

shipper will run on any x86_64 platform, but for best results we recommend running Linux.

To install shipper, Docker and Docker Compose **must** be installed.

A web server (such as Nginx or Apache) should also be installed so that it may serve as a reverse proxy to shipper. This is **required** and should **not** be skipped. Failure to reverse proxy shipper can and will result in security issues, as the reverse proxy of the Docker Compose stack will trust all `X-Forwarded-*` headers sent by the edge reverse proxy. 

## Clone the repository

To install shipper using Docker, first clone this entire repository:

```
git clone --depth=1 https://github.com/shipperstack/shipper
cd shipper
```

## Set up configuration files

The configuration keys and values can be found in the files `docker/example.env` and `docker/example.env.db`. To use them, first copy them:

- `docker/example.env` -> `docker/.env`
- `docker/example.env.db` -> `docker/.env.db`

Then edit the files and adjust the values as necessary. [More information about the configuration options is available here.][configuration]

[configuration]: Configuration.md

## Copy SSH keys

Copy any SSH keys you need to mirror builds to in the `ssh/` directory. (If you don't know what this means, you can make an empty directory and safely skip copying any files into it for now.)

## Create a password for Flower

Flower is a monitoring tool for Celery workers. It is important that you create an access control password to prevent unauthorized access to the Flower instance.

Run the following within the `nginx/` configuration directory:

```
htpasswd -c .htpasswd admin # or any username you prefer
```

## Prepare your terminal environment

Fetch command shortcuts from the activate file:

```
source activate
```

You can run `helpme` if you want to see all the available shortcut commands.

## Start the latest server version

Run:

```
setlatest
dcup
```

to start your shipper instance.

## Initialize the database and collect static files

The database hasn't been initialized yet and the static files need to be collected. Fortunately, a script will do this for us. Run:

```
./django-update.sh
```

And it should automatically apply any unapplied migrations, generate translation files and collect static files for you.


## Create an administrator account

Before you can start configuring and using shipper, you need an administrator account to make any changes in the admin page. Run:

```
dcx web python3 manage.py createsuperuser
```

Done! You should now have an instance of shipper running in Docker. Make any changes to your web server (nginx, Apache, etc.) to reverse-proxy to your shipper instance.