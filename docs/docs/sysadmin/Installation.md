# Installation

Installing shipper is easy with Docker!

Download the following files from this repository:

* `docker-compose.yml`
* `nginx/nginx.conf`

Before installing, create the configuration files by [following the instructions here](Configuration). The configuration files should be in the same folder as the `docker-compose.yml` file. I recommend keeping all the shipper files in a `shipper` directory. At the end, this is how your directory file structure should look like:

* `shipper/`
* `shipper/docker-compose.yml`
* `shipper/.env`
* `shipper/.env.db`
* `shipper/nginx/nginx.conf`
* `shipper/ssh/ssh_keys_here` (required if you will use mirror servers to mirror your builds, otherwise leave the `shipper/ssh/` directory empty)

Once you have everything set up, run the following commands inside the `shipper/` directory:

    export VERSION_TAG=1.13.6 # or latest version from release tab
    docker-compose up -d

By the time you're reading this it's possible there is a new release, so change the `VERSION_TAG` variable above with the latest release found in [GitHub's release tab.](https://github.com/ericswpark/shipper/releases/latest/)

To set up your web server to forward requests to shipper, [follow this reverse proxy guide for nginx](Reverse-Proxy).

If this is the first time you are installing shipper, you may need to run migration on your database and collect the static files:

    docker-compose exec web python manage.py migrate --noinput
    docker-compose exec web python manage.py collectstatic --no-input --clear

This will create a shipper instance with Docker. Once the instance is running, set up a reverse proxy with nginx to the port you specified during configuration.

Set up a superuser within shipper:

    docker-compose exec web python manage.py createsuperuser

Done! Set up shipper in the admin panel.