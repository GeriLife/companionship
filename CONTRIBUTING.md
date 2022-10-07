# Contributing

We welcome many types of contributions, such as the following

- ideas
- bug reports
- code
- design
- community development
- outreach
- project management

## Contributing code

In order to contribute code, you will need to run the project on your local computer.

### Prerequesites

Make sure you have installed the [Poetry](https://python-poetry.org/) package manager before continuing onward in this developer guide.

### CLA

Please [sign our Contributor License Agreement](https://cla-assistant.io/CompanionshipCare/companionship-care) prior to submitting any code.

### Clone the code

You can download or [clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) directly from GitHub, using a command line or [GitHub Desktop](https://desktop.github.com/).

### Environment variables

To run this project locally, you need the following environment variable defined, such by creating a `.env` file with the following contents.

```sh
DJANGO_DEBUG=True
```
We can automatically set the environment variables from the `.env` file when activating the Poetry shell by installing the [Poetry dotenv plugin](https://pypi.org/project/poetry-dotenv-plugin/).

### Install the dependencies

Once you have the project cloned, you can install the project dependencies by running the following command from within the project root directory.

```sh
poetry install
```

### Activate the virtual environment

Once the dependencies are installed, activate the virtual environment with the following command.

```sh
poetry shell
```

### Change into the `project/` subfolter

The following commands should be run from within the `project/` subfolder of this repository. Use your command line tool to change directory into `project/`.

### Run database migrations

Initialize and migrate the project database with the following command.

```sh
python manage.py migrate
```


### Run the project

Create a super-user so you can log into the project.

```sh
python manage.py createsuperuser
```

### Run the server

Run the project with the following command.

```sh
python manage.py runserver
```

### Access the project in your web browser

Once the previous steps are complete and the server is running, visit the following URL in your web browser.

- http://127.0.0.1:8000

### See our .editorConfig file

We use a .editorConfig to keep coding styles consistant between our different developers. See https://editorconfig.org/ for more information.

### Test things out and contribute
 
Now that the project is running, you can try things out and consider how you would like to contribute! :-)

## Testing

### Generate test coverage

Run the following command from within the `project/` directory to generate a test coverage report.

```sh
coverage run --source='.' manage.py test
```

View the coverage report with the following command.

```sh
coverage report
```

## Troubleshooting

### Resolving conflicts in `poetry.lock`

Whenever there are simultaneous changes to our project dependencies, there is a high likelihood of conflicts in poetry.lock. This issue is not unique to our project and likely happens in every Poetry project with multiple developers.

First sync your fork of the repository to keep it up-to-date with upstream.

1. Checkout to the main branch

```sh
git checkout main
```

2. Update main

```sh
git pull
```

3. Checkout to your working branch

```sh
git checkout your-branch
```

4. Merge main branch into your working branch

```sh
git merge main
```

At this point, you may get a conflict in `poetry.lock`. Here are some of the methods you can use to resolve the conflict:

#### Method-1

In order to get `poetry.lock` to look like it does in `main`, you can do the following:

```sh
git checkout --theirs poetry.lock
poetry lock --no-update
```

#### Method-2

1. Delete the `poetry.lock` file
2. Re-generate the `poetry.lock` file by running:

```sh
poetry lock
```
