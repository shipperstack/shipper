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