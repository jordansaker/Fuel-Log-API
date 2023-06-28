# Fuel Log API

![Fuel-log-API](./docs/Fuel_log_API.png) 

## Installation

#### Requirements:
- PostgreSQL
- Python 3

---

#### Database setup

Run PostgreSQL in the terminal:
```
psql
```
Create a database and database user:
```
create database fuel_log_db;
```
```
create user fuel_dev with password 'fueldevpass123';
```
Grant access for the new user to the database:
```
grant all privileges on database fuel_log_db to fuel_dev;
```
---
#### Python setup

In the **src** directory, create a virtual environment and activate it:

```
python3 -m venv .venv
source  .venv/bin/activate
```
Install the required packages:
```
python3 -m pip install -r requirements.txt
```

---

#### Running the Flask application

Rename **.env.sample** to **.env** and add the following configuration and connection to the database.

Using the database name, username, and password above setup the DB URI:
```
DB_URI='postgresql+psycopg2://fuel_dev:fueldevpass123@127.0.0.1:5432/fuel_log_db'
```
Replace SECRET KEY with your secrect key and run the following code  below in the **src** file to setup the .env file:

```
echo "DB_URI='postgresql+psycopg2://fuel_dev:fueldevpass123@127.0.0.1:5432/fuel_log_db'\nJWT_KEY='SECRET KEY'" > .env 
```

The table below lists the available CLI commands for the application.

| CLI commands | Description |
| ----- | ----- |
| flask cli create | Create the the models in the database |
| flask cli drop | Drop the models from the database |
| flask cli seed | Seed the database models with data - Needed to create ADMIN user |
| flask run | Run the Flask application |


Create the models and seed the database. Then run the Flask app in the CLI:

```
flask cli create
flask cli seed
flask run
```

The Flask application is running on the localhost on Port 5000. The endpoints can be accessed through a browser or through API development platforms such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/).

---

## R5    REST API Resources

Below is a full listing of all available endpoints. Click on a resource name for more information. 

#### User Access and account management

| Resource | Description |
| --------------------- | ---------- |
|[POST       /login](./docs/endpoints.md#head1) | Allows existing user to authenticate.|
|[POST       /register](./docs/endpoints.md#head2) | Allows a user to register.|
|[DELETE   /me/$user_id/delete/](./docs/endpoints.md#head3) | Allows a user to delete their account. Admin can delete any user.|

#### Cars

| Resource | Description |
| --------------------- | ---------- |
|[GET               /cars/](./docs/endpoints.md#head4) | Get a list of all cars.|
|[GET               /cars/\$car_id/](./docs/endpoints.md#head23) | Get car.|
|[GET               /cars/$make/](./docs/endpoints.md#head5) | Get a list of all cars by make.|
|[GET               /cars/$make/\$model](./docs/endpoints.md#head6) | Get a list of all cars by make and model.|
|[GET               /cars/me/](./docs/endpoints.md#head7) | Get the list of cars belonging to the user.|
|[GET               /cars/me/$user_car_id/](./docs/endpoints.md#head25) | Get a car that belongs to the user.|
|[POST             /cars/me/](./docs/endpoints.md#head8) | Add a car to the user's list of cars.|
|[DELETE         /cars/me/$user_car_id](./docs/endpoints.md#head9) | Delete a car from the user's car list.|
|[DELETE         /cars/$car_id](./docs/endpoints.md#head10) | ADMIN ONLY:  Delete a car from the car index.|
|[PUT/PATCH   /cars/$car_id](./docs/endpoints.md#head11) | ADMIN ONLY:  Update a car's details.|

#### Logs

| Resource | Description |
| --------------------- | ---------- |
|[GET                 /logs/me/$car_id/](./docs/endpoints.md#head12) | Get the user's logs for the selected car. |
|[GET                 /logs/me/$car_id/\$log_id/](./docs/endpoints.md#head22) | Get a log entry for the selected car. |
|[POST              /logs/me/$car_id/](./docs/endpoints.md#head13) | Add a new log for the selected user car. |
|[PUT/PATCH    /logs/me/$car_id/\$log_id/](./docs/endpoints.md#head14) | Update a log for the selected user car. |
|[DELETE          /logs/me/$car_id/\$log_id](./docs/endpoints.md#head15) | Delete a log for the selected user car. |
|[POST              /logs/me/$car_id/trip/calculator/](./docs/endpoints.md#head16) | Calculate the total fuel cost of a trip. |
|[GET                 /logs/me/$car_id/trips/](./docs/endpoints.md#head17) | Get the user car's list of trips. |
|[GET                 /logs/me/$car_id/trips/\$trip_id/](./docs/endpoints.md#head24) | Get a trip for the user's car. |
|[DELETE           /logs/me/$car_id/trips/\$trip_id](./docs/endpoints.md#head18) | Delete a trip for the selected user car. |
|[PUT/PATCH    /logs/me/$car_id/trips/\$trip_id](./docs/endpoints.md#head19) | Update the trip details for the selected user car. |
|[POST              /logs/me/$car_id/expenditure/](./docs/endpoints.md#head20) | Get the expenditure summary for a time period |
|[POST              /logs/me/$car_id/expenditure/compare/](./docs/endpoints.md#head21) | Compare expenditure summaries for two different periods |

---

## R7    Third Party Services

This API application was created using the Flask web framework, which is a Python module that allows common interface between web servers and web applications. Because Flask was originally developed to have a small and easy-to-extend core: it's seen as a microframework and have out of the box features such as Object Relational Manager (ORM) or other features listed below. [(pythonbasics.org, 2021)](./docs/references.md#R7.1). Here are some of the third party services that were used to fully implement the API.

### SQLAlchemy

The API uses an SQL database system to store data relating to cars, users, and log entries. In order to integrate and allow the Flask app to interact with the database, SQLAlchemy was installed as a dependency and used. SQLAlchemy is the Python ORM that is used by the app to efficiently access and perform database queries interpreting Pythonic language and then creating and executing the equivalent SQL query operation on the database. The approach that SQLAlchemy takes is that it's processes are fully exposed and it allows the developer to construct a database and the SQL queries using Python, almost the same way they would be constructed in an SQL system. [(www.sqlalchemy.org, n.d.)](./docs/references.md#R7.2)

### Flask-SQLAlchemy

Flask has developed an extension for SQLAlchemy to simplify the process of interacting with SQLAlchemy. It automatcally handles creating, using, and cleaning up SQLAlchemy objects. The is done by creating an extension class which then allows for cleaner SQLAlchemy operations through that extension class [(flask-sqlalchemy.palletsprojects.com, n.d.)](./docs/references.md#R7.3). i.e An SQLAlchemy model can be created using the subclass of the extension class:

```
# the extension class
db = SQLAlchemy()
# the subclass db.Model used to define a model class
class User(db.Model)
```

### Marshmallow

The API uses the Marshmallow library to convert complex datatypes, to and from native Python objects. This is done through the Schema class in the Marshmallow library. It allows the app to validate input data, deserialise input data to app-level objects such as Lists or Dicts. It can also serialise app-level objects to be rendered to standard formats such JSON which can then be passed through a request. [(marshmallow.readthedocs.io, n.d.)](./docs/references.md#R7.4)

### Flask-Marshmallow

Similar to Flask-SQLAlchemy, Flask-Marshmallow is also an extension that adds extra features which allow it to be integrated with Marhsmallow and Flask-SQLALchemy. The extension class is integrated with Flask-SQLAlchemy by being initialised after the Flask-SQLAlchemy extension class [(flask-marshmallow.readthedocs.io, n.d.)](./docs/references.md#R7.5). This extension is used to create schema classes which are used when dumping and loading JSON objects. For a schema class, fields are exposed to be dumped or loaded by the schema, and these fields are normally given a Marshmallow specific datatype class. 

### Psycopg2-binary

Psycopg is a PostgreSQL database adapter that can be used for the Python Programming language and was designed to be used for multi-threaded applications [(www.psycopg.org, n.d.)](./docs/references.md#R7.6). It allows the Flask application to connect to the PostgreSQL database, creates and destroys database cursors, and executes queries passed onto it by SQLAlchemy. [(pysql.tecladocode.com, n.d.)](./docs/references.md#R7.7)

### Flask-Bcrypt

Flask-Bcrypt is used as an extension for Flask an provides the app with bcrypt hasshing utilities. Bcrypt uses a hash design that's "de-optimised", making it intentionally structured to be a slow hashing algorithm compared to other algorithms such as MD5 and SHA1. This extension when it is created and initialised in the app, provides a away for sensitive data being pass through the Flask app to be protect. [(flask-bcrypt.readthedocs.io, n.d.)](./docs/references.md#R7.8)

### Flask-JWT-Extended

This Flask extension allows the app to be able to generate JSON Web Tokens. This enables the app to protect routes and allows the app to get the identity of a JWT in a protect route.

### Python-Dotenv

[References](./docs/references.md#R7)

---

#### R1    The problem this API app is trying to solve

This application will provide a way for users to track and record their fuel consuption from bowser to bowser, while providing multiple forecasts and estimations based on their fuel consumption and current fuel costs at the bowsers which will be useful for budgeting purposes.

- The app will help the user budget and plan ahead for fuel expenses for the month
    - It will return the total cost of fuel for a time period and the total distance travelled within that timeframe.
    - Users can also compare expenditure between two different periods.
- The user can calculate the esitmated cost of a trip by providing the distance and the price of fuel
- The average consumption per 100 km is returned each time the user calculates the cost of a trip. This consumption rate is used to estimate the total cost of the trip.
- It allows users to add multiple cars to their list to track separately.

#### R2    Justification for the API

With fuel prices rising steadily over the last 5 years, more car owners are looking for ways to keep running costs down. 

---

## R6    ERD

![Fuel log API ERD](./docs/ERD.png)

---

## R3    Reasons the database system was chosen and its drawbacks


---
## R9     The database relations implemented in the app

#### Entities

The 

- Users
- Log Entries
- Cars
- User Cars
- Trips

---

## R4      Key functionalities and benefits of an ORM

---

## R8      The relationships between the models

---

## R10     Project Management

