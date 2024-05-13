# Troubleshooting

Here are some commons errors and problems you may encounter with shipper, and some potential solutions.

## Permission denied error (Error 13)

If you get a permission denied error while using shipper, it's because the permissions on the volumes that shipper uses have been messed up. This shouldn't happen normally but I've encountered this problem a couple of times and I'm trying to figure out what causes the permissions to get screwed up. For some reason the `media` and `static` folders (and the contents within) all get owned by a `umtp` group, which blocks write access to shipper.

To fix this, fire up a root shell on the container:

    docker exec -u root -it shipper_web_1 sh

Then `chown` the relevant directories:

    chown -R shipper:shipper media/
    chown -R shipper:shipper static/

## shipper lists permissions for nonexistent models

Clean up your database with the following command:

```shell
docker-compose exec web python3 manage.py remove_stale_contenttypes
```

Review the output and answer `yes` to clean up the database.

## I can't connect to shipper / I can't reverse proxy to shipper

Newer Docker Compose files have the network ports bind to the loopback interface (127.0.0.1). This means that if you try and connect to shipper outside of the currently running machine/server, it won't work. This change was made so that you always have to reverse proxy to shipper (in order to avoid any security problems serving shipper over non-HTTPS).

But sometimes, you still run into this issue when reverse proxying to shipper. What gives?

If you're running a second nginx/Apache server on Docker, chances are you're running that container in bridged mode. In this mode, the network is separated from the default network set up by the Docker Compose file of the shipperstack project.

You have a couple of options. First, you can change the network mode of the reverse proxy to host. This will allow the reverse proxy to access shipper through the loopback interface. However, this is not recommended, and may not actually be possible depending on other services you have running on the server.

You can also change the Docker Compose file of the reverse proxy so that it taps into the shipperstack network, like the following:

`docker-compose.yml`:

```yaml
services:
  reverse-proxy-nginx:
    networks:
      - shipper_prod_default

networks:
  shipper_prod_default:
    external: true
```

Make sure to replace both `shipper_prod_default` if you have a different network name.

The solution above may not be possible if your reverse proxy proxies multiple hosts. In that case, you may use the final option below.

Alternatively, you can use an override file. Create the following file in the `docker/` directory and re-up shipper:

`docker-compose.override.yml`:

```yaml
services:
  nginx:
    ports: !override
      - "172.17.0.1:9200:80"
      - "172.17.0.1:9201:81"
```

Replace `172.17.0.1` with the Docker host network.
