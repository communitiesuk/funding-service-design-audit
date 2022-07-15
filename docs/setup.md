# Set-up Service

Clone the repository

## Create a Virtual environment

    python3 -m venv .venv

## Enter the virtual environment

...either macOS using bash:

    source .venv/bin/activate

...or if on Windows using Command Prompt:

    .venv\Scripts\activate.bat

## Install dependencies

requirements-dev.txt and requirements.txt are updated using [pip-tools pip-compile](https://github.com/jazzband/pip-tools)
To update requirements please manually add the dependencies in the .in files (not the requirements.txt files)
Then run (in the following order):

    pip-compile requirements.in

    pip-compile requirements-dev.in

From the top-level directory enter the command to install pip and the dependencies of the project

    python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt

## Initialise and upgrade database
This service is designed to use sqlite for local development and PostgreSQL when deployed.
Both can be easily switched (if required locally) due to the usage of database agnostic ORM SqlAlchemy
This can by done by setting the DATABASE_URL environment variable to the URL of the database you want to test with.

Apply existing migrations to the database:

    flask db upgrade

## Create static files

### Build GovUK Assets

This build step imports assets required for the GovUK template and styling components.
It also builds customised swagger files which slightly clean the layout provided by the vanilla SwaggerUI 3.52.0 (which is included in dependency swagger-ui-bundle==0.0.9) are located at /swagger/custom/3_52_0.

Before first usage, the vanilla bundle needs to be imported and overwritten with the modified files. To do this run:

    python3 build.py

Developer note: If you receive a certification error when running the above command on macOS,
consider if you need to run the Python
'Install Certificates.command' which is a file located in your globally installed Python directory. For more info see [StackOverflow](https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate)
