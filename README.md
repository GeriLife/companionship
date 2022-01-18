# django-bootstrap-quick-start

A Django boilerplate to start your projects faster.

## Copyright

This project is licensed under the [European Union Public License](LICENSE) (EUPL) version 1.2 or later.

More information about the EUPL, including translations in over 20 languages, can be found at the links below.

- [EUPL.eu](https://www.eupl.eu/)
- [EUPL text (EUPL-1.2) | Joinup - European Union](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)

## Thanks

This project was made possible by the following resources.

- Roshan Chokshi [How to Use Email as Username for Django Authentication.](https://dev.to/chokshiroshan/how-to-use-email-as-username-for-django-authentication-8if)
- Will Vincent [Django Best Practices: Custom User Model](https://learndjango.com/tutorials/django-custom-user-model)

## Deployment

This section is a work-in-progress and outlines issues that arise during or relate to deployment. The main assumption is that we are deploying to [Dokku PaaS](https://dokku.com).

### Upload max filesize

In order to upload images, we need to override the Dokku default filesize limit of 1 megabyte.

```sh
dokku nginx:set <dokku-app-name> client-max-body-size 10m
```

After setting `client-max-body-size`, the nginx config needs to be rebuilt.

```sh
dokku proxy:build-config <dokku-app-name>
```
