# Deployment

This section is a work-in-progress and outlines issues that arise during or relate to deployment. The main assumption is that we are deploying to [Dokku PaaS](https://dokku.com).

## Configure initial app and database

Configure the initial Dokku app and database with the following commands.

- create app `dokku apps:create companionship-care-app`
- clear default proxy ports `dokku proxy:ports-clear companionship-care-app`
- configure correct app proxy port `dokku proxy:ports-add companionship-care-app https:443:8000`
- configure app domain `sudo dokku domains:add companionship-care-app <example.com>`
- set `DJANGO_ALLOWED_HOSTS` to include app domain `dokku config:set companionship-care-app DJANGO_ALLOWED_HOSTS=<example.com>`
- set `DJANGO_CSRF_TRUSTED_ORIGINS` to include app domain `dokku config:set companionship-care-app DJANGO_CSRF_TRUSTED_ORIGINS=<https://example.com>`
- install Postgres plugin `dokku plugin:install https://github.com/dokku/dokku-postgres.git`
- create Postgres DB `dokku postgres:create companionship-care-db`
- link DB to app `dokku postgres:link companionship-care-db companionship-care-app`

## Set up SSL

Enable HTTPS support with the following commands on the Dokku server.

- install Let's Encrypt `dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git`
- configure Let's Encrypt email `sudo dokku config:set --no-restart --global DOKKU_LETSENCRYPT_EMAIL=<user@email.com>`
- enable Let's Encrypt for app `sudo dokku letsencrypt:enable companionship-care-app`
- auto-update Let's Encrypt certificate `sudo dokku letsencrypt:cron-job --add`

## Push code from local computer

Now that the Dokku app and database are configured, push code from a local computer to the Dokku server.

- add Git remote on local computer `git remote add dokku dokku@<dokku_server>:django-dokku-example`
- push changes to `dokku` remote `git push dokku main:main`

Follow the prompts to create the initial superuser.

## Create initial Django superuser

Create an initial superuser on the deployed app with the following commands.

- enter the Dokku app `dokku enter companionship-care-app`
- create the Django superuser `python project/manage.py createsuperuser`

## File storage

The following steps will allow persistent file uploads for the Companionship Care app. Below, we assume the Dokku app name is `companionship-care-app` and create a filesystem storage directory with the same name for consistency.

### Create storage directory

Create a Dokku storage directory with the same name as the app, for consistency.

```sh
dokku storage:ensure-directory companionship-care-app
```

### Add local companionship user

Ensure there is a local `companionship` user with the same `uid` as the `companionship` user in the Docker container.

```sh
useradd companionship --uid 33777
```

### Change ownership of storage directory

Ensure the storage directory is owned by the `companionship` user.

```sh
chown companionship /var/lib/dokku/data/storage/companionship-care-app
```

```sh
chgrp companionship /var/lib/dokku/data/storage/companionship-care-app
```

### Mount the storage container into the Docker image

Ensure the storage directory is mounted to the `MEDIA_ROOT` directory within the Docker container.

```sh
dokku storage:mount companionship-care-app /var/lib/dokku/data/storage/companionship-care-app:/app/project/media
```

### Restart the app

The app needs to be restarted in order for changes to take effect.

```sh
dokku ps:restart companionship-care-app
```

### Upload max filesize

In order to upload images, we need to override the Dokku default filesize limit of 1 megabyte.

```sh
dokku nginx:set companionship-care-app client-max-body-size 10m
```

After setting `client-max-body-size`, the nginx config needs to be rebuilt.

```sh
dokku proxy:build-config companionship-care-app
```
