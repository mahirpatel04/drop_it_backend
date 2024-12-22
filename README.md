# DropIt Backend

This is the backend repository for the DropIt app. There is a basic guideline to follow so that you can read, contribute, and understand the code.


# Folder Structure

- alembic/
- app/
	- core/
	- database/
	- models/
	- routers/
	- schemas/
	- services
	- utils
	- init.py
	- main.py
- tests/
- .env
- .env.SAMPLE
- .gitignore
- alembic.ini
- README.md
- requirements.txt

## Folder Descriptions

### Alembic:
Used for database migrations. Allows us to upgrade the database models and columns easily.

To include generate a migration file for your new changes: `alembic revision --autogenerate -m "include your message here"`

To upgrade your database to the latest version based on the migration files: `alembic upgrade head`
### App:
Main folder which contains the actual application files
#### Core:
Contains the configuration files to instantiate app level settings and creating the logger.
#### Database:
Sets up the connection between the app and the database. We have already created a local database using postgresql but this allows for communication between the database and the app.
#### Models:
Sets up the models that we will use in the Database  such as the different tables, columns, and parameters of a certain model. Alembic will use this folder to create the migration files.
#### Routers:
The actual endpoints are written in this folder. They are split into different folders depending on their functionality.

An endpoint should be written a specific way. It should contain dependencies like the User if they need to be logged in to perform the action and the Database if some data is going to be fetched, updated, deleted, etc. There should be no logic in the endpoints. Everything should be wrapped in a try-except block where a service function is called. The service function will throw appropriate errors and the the try-except blocks will catch these errors and raise the appropriate HTTP Exceptions.

#### Schemas:
Schemas for responses and payloads are written here. These responses and payloads are used for passing into endpoints and returning from the endpoints.
#### Services:
This is where the logic of the endpoints is held. The folder is split into files depending on which routers are using the functions in the files. The files contain functions that the endpoints will call. These functions throw errors and the endpoints will catch these errors and in turn raise appropriate HTTP Exceptions.
#### Utils:
General utility functions and pieces go in here. Exceptions.py includes custom errors that the app uses in the endpoints/service functions.
### Tests
Contains the testing framework for the application. We are using pytest to do our testing. You can run the tests by using: `pytest`

To generate a coverage report you can use the following command: `pytest --cov=app  tests/`
- app is because that is the module we want to generate the coverate report for
- tests/ is where the tests are stored

You can generate an html version of the coverage report which shows excatly which lines of the code have been tested and which havent using the following command: `pytest --cov --cov-report=html`

Then a folder called htmlcov will be created which contains a file called index.html. You can open this file in the browser and go through this for the detailed coverage report.