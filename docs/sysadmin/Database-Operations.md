# Database Operations

## Using `django-dbbackup`

### Warning

This method is still in beta! The restore may not be successful.

Please back up using alternative methods before doing anything destructive, like deleting the main database volume!

### Dump

To create a dump of the database, make sure that the web and database services are running. If they are not running, start them with:

```
docker compose up -d web db
```

Then run:

```
docker compose exec web python3 manage.py dbbackup
docker compose exec web ls /tmp/shipper-backup
```

Copy the file name, and then use the following command to copy the backup file to your host:

```
docker compose cp web:/tmp/shipper-backup/<FILE NAME HERE> .
```

### Restore

Copy the file back into the container:

```
docker compose exec web mkdir -p /tmp/shipper-backup
docker compose cp ./<FILE NAME HERE> web:/tmp/shipper-backup/
```

Then restore using the following command:

```
docker compose exec web dbrestore
```


## Using raw PostgreSQL

### Dump

To create a dump of the database, make sure the database service is first running. If it is not running, start it with:

```
docker compose up -d db
```

Then run:

```
docker compose exec db pg_dumpall -U pdbuser > dump.sql
```

Make sure to substitute `db` and `pdbuser` if you have customized those in the Docker Compose file or in the environment file.

You should now have a dump file called `dump.sql` in your current directory. Now is the time to make any changes, such as deleting the database volume, upgrading the PostgreSQL version, and so on. If you have made the necessary changes, move on to the next section.

### Restore

To restore a dump of the database, first start up the shipper-docker instance and make sure the PostgreSQL database is running. Make sure you are in the directory with the `dump.sql` file. Execute:

```
# Copy the dump file to the volume by spinning up a temporary Docker image (seriously Docker team why the hell do we have to do this?!)
docker run --rm -v shipper_postgres_data:/target -v $(pwd):/source alpine cp /source/dump.sql /target

# Connect to the current database instance inside the Docker Compose file
docker compose exec db bash

# Import
psql -U pdbuser -d shipper < /var/lib/postgresql/data/dump.sql

# Delete the dump file
rm /var/lib/postgresql/data/dump.sql
```

Make sure to substitute `shipper_postgres_data`, `pdbuser`, and `shipper` if you have customized those in the Docker Compose file or in the environment files.

#### I'm getting an authentication error from Django

Sometimes, after loading from the dump, the server may display a 500 error, with the Django logs indicating an authentication problem connecting to the database. In this case, it could be that the database dump did not contain the correct authentication details or the details failed to carry over during the loading step.

To fix this issue, simply set the password of the PostgreSQL user again with the credentials in `.env.db`, like so:

```
# Connect to the current database instance inside the Docker Compose file
docker compose exec db bash

# Connect to PostgreSQL
psql -U pdbuser

# Change password
ALTER USER pdbuser PASSWORD 'hunter2';

# Exit
\q
```

Make sure to substitute `pdbuser` and `hunter2` (obviously) from the environment files.

## Using Docker volumes

You can back up the entire Docker volume to make a backup of the database.

Note that PostgreSQL database backups made using this method are not usable on different versions! In short, you won't be able to take a backup made on 14.3 and use it on 15.2, or anything like that.

```
docker volume create --name shipper_postgres_data_backup_ver
docker run --rm -it -v shipper_postgres_data:/from -v shipper_postgres_data_backup_ver:/to alpine ash -c "cd /from ; cp -av . /to"
# If starting over
docker volume rm shipper_postgres_data
```
