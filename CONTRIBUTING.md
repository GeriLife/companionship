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

Please [sign our Contributor License Agreement](https://contributoragreements.org/query2form/?_replyto=support@companionship.care&_subject=Contributor%20License%20Agreement%20E-Signing&_body=Fill%20out%20the%20following%20form,%20then%20sign%20your%20initials%20to%20complete%20the%20Contributor%20License%20Agreement.&agreement-type[]=individual&agreement-type[]=entity&fullname=&title=&company=&email-address=&physical-address=&your-initials=&signed-agreement_s=%3Fyour-date%3D%40_time%26your-name%3D%40fullname%26your-title%3D%40title%26your-address%3D%40email-address%26your-patents%3D%40Patent-IDs-and-Country_t%26process-url%3D%40_processurl%26action%3Dsign-%40agreement-type%26%40u2s&_processurl=@processurl&_action[0]=http://contributoragreements.org/query2email/&_action[1]=http://contributoragreements.org/query2update/&_next=View%20More%20Contributor%20License%20Agreement%20Signers.&_success=Thank%20you%20for%20using%20contributoragreements.org.%20The%20agreement%20has%20been%20signed%20and%20sent%20via%20E-Mail%20and%20will%20not%20be%20stored.&_submit=Sign%20Your%20Contributor%20License%20Agreement.) prior to submitting any code.

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
