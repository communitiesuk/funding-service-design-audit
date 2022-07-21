# Run Service

Then run:

    flask run

A local dev server will be created on

    http://127.0.0.1:5000/

This is configurable in .flaskenv

To see the API swagger documentation,  navigate to:

    http://127.0.0.1:5000/

### Making changes to the database

Whenever you make changes to database models, please run:

    flask db migrate

This automatically detects the scripted database changes and updates the migration folder (/db/migrations).

Then apply the new migrations to the database:

    flask db upgrade

Then each time the database models change repeat the migrate and upgrade commands.

Please then commit and push these to github so that the migrations will be run in the pipelines to correctly
upgrade the deployed db instances with your changes.


### Run with Gunicorn

In deployed environments the service is run with gunicorn. You can run the service locally with gunicorn to test

First set the FLASK_ENV environment you wish to test eg:

    export FLASK_ENV=dev

Then run gunicorn using the following command:

    gunicorn wsgi:app -c run/gunicorn/local.py
