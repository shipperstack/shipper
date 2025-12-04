# Backup

## Database

You can use `django-dbbackup`'s `dbbackup` command to create a backup.


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

The output should be something like `default-<ID>-2025-12-04-173031.psql.bin`.

Copy the file name, and then use the following command to copy the backup file to your host:

```
docker compose cp web:/tmp/shipper-backup/<FILE NAME HERE> .
```

Note the `.` at the end to copy to the current directory. You can replace it with the desired target directory.

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


## Media


You can use `django-dbbackup`'s `mediabackup` command to create a backup.


### Dump

To create a dump of the media files, make sure that the web and database services
are running. If they are not running, start them with:

```
docker compose up -d web db
```

Then run:

```
docker compose exec web python3 manage.py mediabackup
docker compose exec web ls /tmp/shipper-backup
```

The output should be something like `default-<ID>-2025-12-04-173031.psql.bin`.

Copy the file name, and then use the following command to copy the backup file
to your host:

```
docker compose cp web:/tmp/shipper-backup/<FILE NAME HERE> .
```

Note the `.` at the end to copy to the current directory. You can replace it with
the desired target directory.

### Restore

Copy the file back into the container:

```
docker compose exec web mkdir -p /tmp/shipper-backup
docker compose cp ./<FILE NAME HERE> web:/tmp/shipper-backup/
```

Then restore using the following command:

```
docker compose exec web mediarestore
```