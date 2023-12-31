# Fuel Log API

![Fuel-log-API](./docs/screenshots/Fuel_log_API.png)

---

- [GitHub Repo Link](https://github.com/jordansaker/Fuel-Log-API)
- [Installation](#installation)
- [Rest API Resources](#r5-rest-api-resources)
    - [User Access and account management](#user-access-and-account-management)
    - [Cars](#cars-1)
    - [Logs](#logs)
- [Third Party Services](#r7-third-party-services)
- [ERD](#r6erd)
- [The database relations implemented in the app](#r9-the-database-relations-implemented-in-the-app)
    - [Entities](#entities)
        - [Users](#users)
        - [User Cars](#user-cars)
        - [Log Entries](#log-entries)
        - [Cars](#car)
        - [User Trips](#user-trips)
    - [Cars and Users:   Many to Many Relationship](#cars-and-users-many-to-many-relationship)
    - [User Cars and Log Entries: One to Many Relationship](#user-cars-and-log-entries-one-to-many-relationship)
    - [User Cars and User Trips: One to Many Relationship](#user-cars-and-user-trips-one-to-many-relationship)
- [PostgreSQL:  Reasons the database system was chosen and its drawbacks](#r3-postgresql-reasons-the-database-system-was-chosen-and-its-drawbacks)
- [Key functionalities and benefits of an ORM](#r4-key-functionalities-and-benefits-of-an-orm)
- [The relationships between the models in the app](#r8-the-relationships-between-the-models-in-the-app)
- [Project Management](#r10-project-management)

---

## Installation

#### Requirements:
- PostgreSQL
- Python 3

---

#### Database setup

Run PostgreSQL in the terminal:
```sh
psql
```
Create a database and database user:
```sh
create database fuel_log_db;
```
```sh
create user fuel_dev with password 'fueldevpass123';
```
Grant access for the new user to the database:
```sh
grant all privileges on database fuel_log_db to fuel_dev;
```
---
#### Python setup

Clone the repo to a local directory:

```sh
git clone https://github.com/jordansaker/Fuel-Log-API.git
```

In the **src** directory, create a virtual environment and activate it:

```sh
python3 -m venv .venv
source  .venv/bin/activate
```
Install the required packages:
```sh
python3 -m pip install -r requirements.txt
```

---

#### Running the Flask application

Rename **.env.sample** to **.env** and add the following configuration and connection to the database. Using the database name, username, and password above setup the DB URI:
```sh
ENVIRONMENT='dev'
DB_URI_DEV='postgresql+psycopg2://fuel_dev:fueldevpass123@127.0.0.1:5432/fuel_log_db'
```
Replace SECRET KEY with your secrect key and run the following code  below in the **src** file to setup the .env file:

```sh
echo "# Environment. Change to "dev" or "prod"\nENVIRONMENT='dev'\n# This is the database configuration and connection for production\nDB_URI=''\n# This is the database configuration and connection for development\nDB_URI_DEV='postgresql+psycopg2://fuel_dev:fueldevpass123@127.0.0.1:5432/fuel_log_db'\n# This is the JWT key\nJWT_KEY='SECRET KEY'" > .env 
```

To add a production database, add the production database configuration URL to DB_URI in the **.env** and change the ENVIRONMENT to 'prod'.

#### Production server

The app uses Gunicorn as a production server. To run the production server locally:

```sh
gunicorn -w 4 "app:create_app()"
```

##### CLI Commands

The table below lists the available CLI commands for the application.

| CLI commands | Description |
| ----- | ----- |
| flask cli create | Create the the models in the database |
| flask cli drop | Drop the models from the database |
| flask cli seed | Seed the database models with data - Needed to create ADMIN user |
| flask run | Run the Flask application |


Create the models and seed the database. Then run the Flask app in the CLI:

```sh
flask cli create
flask cli seed
flask run
```

The Flask application is running on the localhost on Port 5000. The endpoints can be accessed through a browser or through API development platforms such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/).

##### Seeded Users
|email |password| admin |
| ---- | ---- | ---- |
| fuellogadmin@fuellogapi.com | admin1234 | True |
| john.smith@test.com | password123 | False |
| will.thomas@gmail.com | thisIsapassword | False |

---

## R5 REST API Resources

Below is a full listing of all available endpoints. Click on a resource name for more information.

#### User Access and account management

| Resource | Description |
| --------------------- | ---------- |
|[POST       /login](./docs/endpoints.md#post-login) | Allows existing user to authenticate.|
|[POST       /register](./docs/endpoints.md#post-register) | Allows a user to register.|
|[GET         /users/](./docs/endpoints.md#get-users) | ADMIN ONLY: Allows admin to get all users details|
|[DELETE   /me/$user_id/delete/](./docs/endpoints.md#delete-meuser_iddelete) | Allows a user to delete their account. Admin can delete any user.|

#### Cars

| Resource | Description |
| --------------------- | ---------- |
|[GET               /cars/](./docs/endpoints.md#get-cars) | Get a list of all cars.|
|[GET               /cars/\$car_id/](./docs/endpoints.md#get-carscar_id) | Get car.|
|[GET               /cars/$make/](./docs/endpoints.md#get-carsmake) | Get a list of all cars by make.|
|[GET               /cars/$make/\$model](./docs/endpoints.md#get-carsmakemodel) | Get a list of all cars by make and model.|
|[GET               /cars/me/](./docs/endpoints.md#get-carsme) | Get the list of cars belonging to the user.|
|[GET               /cars/me/$user_car_id/](./docs/endpoints.md#get-carsmeuser_car_id) | Get a car that belongs to the user.|
|[POST             /cars/me/](./docs/endpoints.md#post-carsme) | Add a car to the user's list of cars.|
|[DELETE         /cars/me/$user_car_id](./docs/endpoints.md#delete-carscar_id) | Delete a car from the user's car list.|
|[DELETE         /cars/$car_id](./docs/endpoints.md#delete-carscar_id) | ADMIN ONLY:  Delete a car from the car index.|
|[PUT/PATCH   /cars/$car_id](./docs/endpoints.md#putpatch-carscar_id) | ADMIN ONLY:  Update a car's details.|

#### Logs

| Resource | Description |
| --------------------- | ---------- |
|[GET                 /logs/me/$user_car_id/](./docs/endpoints.md#get-logsmeuser_car_id) | Get the user's logs for the selected car. |
|[GET                 /logs/me/$user_car_id/\$log_id/](./docs/endpoints.md#get-logsmeuser_car_idlog_id) | Get a log entry for the selected car. |
|[POST              /logs/me/$user_car_id/](./docs/endpoints.md#post-logsmeuser_car_id) | Add a new log for the selected user car. |
|[PUT/PATCH    /logs/me/$user_car_id/\$log_id/](./docs/endpoints.md#putpatch-logsmeuser_car_idlog_id) | Update a log for the selected user car. |
|[DELETE          /logs/me/$user_car_id/\$log_id](./docs/endpoints.md#delete-logsmeuser_car_idlog_id) | Delete a log for the selected user car. |
|[POST              /logs/me/$user_car_id/trip/calculator/](./docs/endpoints.md#post-logsmeuser_car_idtripcalculator) | Calculate the total fuel cost of a trip. |
|[GET                 /logs/me/$user_car_id/trips/](./docs/endpoints.md#get-logsmeuser_car_idtrips) | Get the user car's list of trips. |
|[GET                 /logs/me/$user_car_id/trips/\$trip_id/](./docs/endpoints.md#get-logsmeuser_car_idtripstrip_id) | Get a trip for the user's car. |
|[DELETE           /logs/me/$user_car_id/trips/\$trip_id](./docs/endpoints.md#delete-logsmeuser_car_idtripstrip_id) | Delete a trip for the selected user car. |
|[PUT/PATCH    /logs/me/$user_car_id/trips/\$trip_id](./docs/endpoints.md#putpatch-logsmeuser_car_idtripstrip_id) | Update the trip details for the selected user car. |
|[POST              /logs/me/$user_car_id/expenditure/](./docs/endpoints.md#post-logsmeuser_car_idexpenditure) | Get the expenditure summary for a time period |
|[POST              /logs/me/$user_car_id/expenditure/compare/](./docs/endpoints.md#post-logsmeuser_car_idexpenditurecompare) | Compare expenditure summaries for two different periods |

## [REST API Resource](./docs/endpoints.md)

---

## R7 Third Party Services

This API application was created using the Flask web framework, which is a Python module that allows common interface between web servers and web applications. Because Flask was originally developed to have a small and easy-to-extend core: it's seen as a microframework and has out of the box features such as an Object Relational Mapper (ORM) or other features listed below. [(pythonbasics.org, 2021)](./docs/references.md#r7). Here are some of the third party services that were used to fully implement the API.

### SQLAlchemy

The API uses an SQL database system to store data relating to cars, users, and log entries. In order to integrate and allow the Flask app to interact with the database, SQLAlchemy was installed as a dependency and used. SQLAlchemy is a Python ORM that's used by the app to efficiently access and perform database queries interpreting Pythonic language and then creating and executing the equivalent SQL query operation on the database. The approach that SQLAlchemy takes is that it's processes are fully exposed and it allows the developer to construct a database and SQL queries using Python alone, almost the same way they would be constructed in an SQL system. [(www.sqlalchemy.org, n.d.)](./docs/references.md#r7)

### Flask-SQLAlchemy

Flask has developed an extension for SQLAlchemy to simplify the process of interacting with SQLAlchemy. It automatically handles creating, using, and cleaning up SQLAlchemy objects. The is done by creating an extension class which then allows for cleaner SQLAlchemy operations through that extension class [(flask-sqlalchemy.palletsprojects.com, n.d.)](./docs/references.md#r7). i.e An SQLAlchemy model can be created using the subclass of the extension class:

```python
# the extension class
db = SQLAlchemy()
# the subclass db.Model used to define a model class
class User(db.Model)
```

### Marshmallow

The API uses the Marshmallow library to convert complex datatypes, to and from native Python objects. This is done through the Schema class in the Marshmallow library. It allows the app to validate input data and deserialise input data to app-level objects such as Lists or Dicts. It can also serialise app-level objects to be rendered to standard formats such JSON which can then be passed on through a request. [(marshmallow.readthedocs.io, n.d.)](./docs/references.md#r7)

### Flask-Marshmallow

Similar to Flask-SQLAlchemy, Flask-Marshmallow is also an extension that adds extra features which allow it to be integrated with Marhsmallow and Flask-SQLALchemy. The extension class is integrated with Flask-SQLAlchemy by being initialised after the Flask-SQLAlchemy extension class [(flask-marshmallow.readthedocs.io, n.d.)](./docs/references.md#r7). This extension is used to create schema classes which are used when dumping and loading JSON objects. For a schema class, fields are exposed to be dumped or loaded by the schema, and these fields are normally given a Marshmallow specific datatype class. 

### Psycopg2-binary

Psycopg is a PostgreSQL database adapter that can be used for the Python Programming language and was designed to be used for multi-threaded applications [(www.psycopg.org, n.d.)](./docs/references.md#r7). It allows the Flask application to connect to the PostgreSQL database, creates and destroys database cursors, and executes queries passed onto it by SQLAlchemy. [(pysql.tecladocode.com, n.d.)](./docs/references.md#r7)

### Flask-Bcrypt

Flask-Bcrypt is used as an extension for Flask and provides the app with bcrypt hashing utilities. Bcrypt uses a hash design that's "de-optimised", making it intentionally structured to be a slow hashing algorithm compared to other algorithms such as MD5 and SHA1. This extension when it's created and initialised in the app, provides a way for sensitive data being passed through the Flask app to be protected. [(flask-bcrypt.readthedocs.io, n.d.)](./docs/references.md#r7)

### Flask-JWT-Extended

This Flask extension allows the app to be able to generate JSON Web Tokens. This enables the app to protect routes and allows the app to get the identity of a JWT in a protected route. As with Flask-SQLAlchemy, Flask-Bcrypt, and Flask-Marshmallow, its utilities are made available after an extension class is created in the app. The app is secured by being configured with a JWT secret key, which is added to the JWT bearer token each time a user authenticates. [(flask-jwt-extended.readthedocs.io, n.d.)](./docs/references.md#r7)

### Python-Dotenv

This third party service is used for reading key-value pairs from .env files and sets these pairs as environment variables which can be accessed by an application [(Kumar, n.d.)](./docs/references.md#r7). Python-Dotenv was used to read the .env file in the application src directory which was setup to configure the database URI and the JWT secret ket. An example of how these app properties would be configured from an .env file and accessed using Python-Dotenv is shown below.

![.env.sample](./docs/screenshots/env_sample.png)
**Fig. 1**

[References](./docs/references.md#r7)

---

#### R1 The problem this API app is trying to solve

This application will provide a way for users to track and record their fuel consumption from bowser to bowser. It will provide multiple forecasts and estimations based on their fuel consumption and current fuel costs at the bowsers, which will be useful for budgeting purposes.

- The app will help the user budget and plan ahead for fuel expenses for the month.
    - It will return the total cost of fuel for a time period and the total distance travelled within that timeframe.
    - Users can also compare expenditure between two different periods.
- The user can calculate the esitmated cost of a trip by providing the distance and the price of fuel.
- The average consumption per 100 km is returned each time the user calculates the cost of a trip. This consumption rate is used to estimate the total cost of the trip.
- It allows users to add multiple cars to their list to track separately.

#### R2 Justification for the API

With fuel prices rising steadily over the last 5 years, more car owners are looking for ways to keep running costs down.

- Users can have better control over living expenses.
- Car usage and running costs records can be stored and retrieved efficiently compared to a basic spreadsheet.
- The API can be extended to accommodate transport businesses since it already allows users to add multiple cars to track. 

---

## R6 ERD

![Fuel log API ERD](./docs/screenshots/ERD.png)

**Fig. 2**: Fuel Log API ERD

---

## R9 The database relations implemented in the app

#### Entities

The following entities were designed using an [ERM](./docs/screenshots/ERM.png) and the ERD in Fig. 2 above to conceptualise the relations between them.

- Users
    -   
    - The users entity contains records of users who are able to access the API endpoints. When a user registers, they provide an email and password. There can only be one record associated with an email, while the user doesn't have to provide a first and last name. A user is assigned a boolean value based on whether they're an administrator or not. The defualt value when a user is created is False.
    
![users-user-car](./docs/screenshots/users-user-cars.png)
**Fig. 3**: Users and User Cars in [ERD](#r6-erd)

- User Cars
    -
    - User cars is a join table for the Users and Cars entities and each record contains a user ID and car ID.

- Log Entries
    - 
    - The log entries entity contains the records of all log entries for all user cars. For the attributes, seen in Fig. 4 below, "current_odo", "fuel_quantity", and "fuel_price" require user inputs while the date for each log is automatically added each time a new record is created.

![log-entries-user-car](./docs/screenshots/log_entries_user_car.png)
**Fig. 4**: Log Entries and User Cars in [ERD](#r6-erd)

- Cars
    -
    - The cars entity contains records of car types that a user may have. Every attribute has the NOT NULL property while a three column key constraint is placed on the entity using "make", "model", "model_trim", "year", "tank-size". 

![cars-user-trips](./docs/screenshots/cars_user_trips.png)
**Fig. 5**: Cars and User Trips in [ERD](#r6-erd)

- User Trips
    -
    - In the user trips entity (Fig. 5 above), a user car and distance travelled for the trip plus the cost of fuel is stored in each record. Both distance and fuel price have the NOT NULL property.

##### Cars and Users: Many to Many Relationship

The relationship between the cars and users entities is a many to many relationship. A user can have many cars and a car of a specific make, model, and model trim can be owned by many users. Because of this relationship between users and cars, a joining table called "user_cars" was created. This joining table allowed a one to many relationship for the users and cars entities i.e. a user can have many "user_cars" and a car can belong to many "user_cars". 

As seen in Fig. 6 below, a user can have zero or many user cars and a user car belongs to only one user. A car type on the other end can be owned by zero or many users and a user car has only one specific car type.

![users-cars-many](./docs/screenshots/users-cars-many.png)
**Fig. 6**: Cars and User Trips many to many in [ERD](#r6-erd)

##### User Cars and Log Entries: One to Many Relationship

User cars and log entries have a one to many relationship. A user car can have many log entries while a log entry belongs to only one user car. As seen in Fig. 7 below, a user car can have zero or many log entries while a log entry bleongs to only one user car.

![log-entries-user-car](./docs/screenshots/log_entries_user_car.png)
**Fig. 7**: Log Entries and User Cars one to many in [ERD](#r6-erd)

##### User Cars and User Trips: One to Many Relationship

The relationship between user cars and user trips is a one to many relationship. A user car can have many trips while a trip belongs to only one user car. As seen in Fig. 8 below, a user car can have zero or many user trips while a user trip only has one user car.

![cars-user-trips](./docs/screenshots/cars_user_trips.png)
**Fig. 8**: Cars and User Trips one to many in [ERD](#r6-erd)

---

## R3 PostgreSQL: Reasons the database system was chosen and its drawbacks

The main reasons for using PostgreSQL is its high data consistency and integrity which allows it to have excellent transaction processing and data analysis capabilities. This means that PostgreSQL's features are always compliant with the Atomicity, Consistency, Isolation, and Durability model (ACID), which ensures that transactions made are correct and reliable when writing or updating data [(cleancommit.io, 2022)](./docs/references.md#r3). Because of this, Postgres excels when it comes to performance when writing to the database. 

Compare this to MySQL where it is only ACID compliant when used with other storage engines such as InnoDB and NDB Cluster. MySQL uses write locks, meaning only one user can edit the table, making other users wait for the operation to finish [(Amazon Web Services, Inc., n.d.)](./docs/references.md#r3). For an app that's designed to have multiple users edit a table, this poses a problem if MySQL was to be used.  

The read performace of Postgres is more memory-intensive, creating a new process for every user that's connected to the database. This is a drawback that's comparable to MySQL which uses a single process for multiple users [(Amazon Web Services, Inc., n.d.)](./docs/references.md#r3). The trade-off for better write speed over slow read speed suits the operation of the API which is designed to have users write to the database more often than reading from the database.  

Postgres' atomicity feature means that a transaction is completely successful or it fails completely [(cleancommit.io, 2022)](./docs/references.md#r3). Meaning if a post transaction to the database doesn't meet predefined constraints such as a value violating a unique constraint (intergrity error), the transaction completely fails and data entries in the incomplete transaction remains unchanged in the database (an immediate rollback of the transaction). The atomcity feature was useful in the app in certain places such as setting a unqiue constraint for the user email and a key constraint that was a combination of car make, model, model trim, year, tank size. This ensured that incomplete data wasn't added to the database when the violation of these constraints occured.

The consistency feature of Postgres ensures that during transactions, the database can only be changed from a valid state to another. This gurantess that the final state of the database remains consistent as it was before a transaction [(cleancommit.io, 2022)](./docs/references.md#r3). In the app for example, if a user was to be deleted, a cascading delete has to be defined to ensure that data in the user cars table remained the same; i.e user_id was set as NOT NULL so the records relating to the deleted user had to be deleted to ensure no records contained a NULL value in the user_id column.

Isloation in Postgres ensures that many transactions can happen simultaneously. A common type of simultaneous transaction that could happen is reading and writing to the database at the same time [(cleancommit.io, 2022)](./docs/references.md#r3). The final feature, durability, ensures that the transactions that have been committed will permanently survive in the database [(cleancommit.io, 2022)](./docs/references.md#r3). This property of Postgres suits the requirements of this app in that data that is committed to the database will be permanent. It ensures that records containing logs, which are cruical for the core feature of the app, will not be lost. 

The major drawback or challange with Postgres is that it uses an approach called multi-version concurrency control (MVCC) [(cleancommit.io, 2022)](./docs/references.md#r3). A basic idea of this approach in one instance is during an UPDATE, instead of selecting the actual row in the database to write too, a new row is created initally and is only visible to the transaction. Once the transaction is commited, that new row becomes visible to all new transactions. However, transactions that were still occuring at the time of the new row being create will not be able to access this new row. But to satisfy the isolation feature of the database, the old record can still be accessed by the current transactions. This leads to a storage management problem. The old records end up being "dead" rows or Dead Tuples, even though Dead Tuples can no longer be selected by the user, they still exist in the Postgres database paired to their new row. [(EDB, n.d.)](./docs/references.md#r3)

The database esentially could grow with no limit on the size, using up valuable storage space. Because of this side product of MVCC, a process called VACUUM is used to remove dead rows from the database. And since dead rows are created during many processes occuring in or to the database i.e. updating records or incomplete transactions; VACCUM is necessary to maintain a Postgres database [(EDB, n.d.)](./docs/references.md#r3). MySQL in comparison has no need for dead row maintenance as it does not offer MVCC.[(Amazon Web Services, Inc., n.d.)](./docs/references.md#r3)

[References](./docs/references.md#r3)

---

## R4 Key functionalities and benefits of an ORM

### Functionalities

An Object Relational Mapper's key function is to create a mapping or "bridge" between Object Oriented Programming (OOP) and relation databases. The need for this bridging is due to relation databases designed on the basis of mathematical principles (set theory, first-order logic), while the OOP princples are based on Encapsulation, Data Abstraction, Polymorphism and Inheritance. [(Sarkar, n.d.)](./docs/references.md#r4)

An ORM is able to map tables in the relational database to class objects or models. Table columns in databases then map as class attributes, while a record within a table is mapped as an instance of the class. This now allows an OOP language to manipulate a relation database table and records within the table using only objects in the native programming language. It essentially removes the need for a back-end language to directly interact with database tables through SQL queries. For example, if a table "users" within a database existed and was mapped by an ORM to be the model "User" in Python, a new user would be created using the following line of code:

```python
new_user = User(
    name = "John Smith",
    age = 20,
)
```
This instance can then be used to update the database through the ORM. If a record within "users" in the database existed:
```
id |    name    | age |
---| ---------- | --- |
1  | John Smith |  20 |
```
An ORM is able to retrive that record and present it to the programming environment as an object as shown below:

```python
{
    "id": 1,
    "name": "John Smith",
    "age": 20
}
```
So an ORM can be used to perform CRUD operations on relational databases without the need for embbeding database query language (SQL) within the the back-end programming language. It creates this abstraction within an app, removing the underlying querying processes that would occur to a database and providing utilities (methods) that can be used in place of query language. A query of the database using an ORM would look something like this:

```python
user = User.query.where(User.id == 1)
```
The ORM then executes the query on the "users" table in the database to return the user matching the condition. The ORM takes the record and returns it as an object which is assigned to the variable "user". The create, update, and delete operations are normally added to transactions and the ORM commits these transactions to the database.

### Benefits
One of the benefits of using an ORM is that it makes it eaiser for an app design to follow the MVC design process (Fig. 9 below). It naturally adds the model layer to the process and separates the models from the controller and routes. This natural separation of concerns forces the controller to manipulate the mapped models created which in turn updates the the database accordingly. And because this design pattern is implemented with ORMs, it makes the app more transferrable such as changing database systems or the controller language. Since the data models are all in one place, it makes them easier to update, maintain, and reuse the code. This is a major benefit in terms of being cost-effective and increasing productivity by removing code that would otherwise have had to be handwritten. For this very reason, ORMs are often chosen to speed up development time.

![MVC-design](./docs/screenshots/MVC.png)
**Fig. 9**: MVC design [(Amin, 2022)](./docs/references.md#r4)

The abstraction of SQL from the back-end programming language by an ORM adds a layer of protection for the database. Even though using an ORM doesn't make an app completely immune from SQL injections [(snyk.io, n.d.)](./docs/references.md#r4), when used along with other practices such as input validation and prepared statements, it takes away the vast majority of risks regarding SQL Injection.

[References](./docs/references.md#r4)

---

## R8 The relationships between the models in the app

The models contained in the app are mapped to reflect the entities that were designed in the [ERD](#r6-erd). The model User relates to the UserCar model as a one to many relationship, the many side of the relationship is linked to the UserCar model. To create this relationship between the models, the foreign key user_id was added to the UserCar model (shown below).

```python
    
# model atributes
id = db.Column(db.Integer, primary_key=True)
# Foreign Keys
user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
car_id = db.Column(
        db.Integer,
        db.ForeignKey('cars.id', ondelete='CASCADE'),
        nullable=False
    )

```

To establish a bi-directional relationship between the two models, a related field was declared in the User model using the relationship() with reference to the UserCar model (shown below). Models in the app that contain a foreign key have this bi-directional relationship.

```python
# relationships to foreign key in other table (not model defined attributes)
cars = db.relationship('UserCar', backref='user')
```
This now links the User and UserCar models together. So when this relationship is established, "cars" can be exposed in the User schema even though it's not defined as a model attribute. But the main idea behind the relationship() is that if a new user car was to be added to the database, it could be done through the User model by appending a new UserCar instance via the "cars" relationship defined in the User class model. And this update in the User model will create an update in the UserCar model and add it to the session ready to be committed to the database [(docs.sqlalchemy.org, n.d.)](./docs/references.md#r8). Another property of the relationship function is that it allows for the relating model data to be nested in the User schema (shown below). From the User object, a list of related UserCar objects can be access.

```python
cars = fields.List(fields.Nested(
                'UserCarSchema', 
                exclude=['id', 'logs', 'user_id']
            ))
...
fields = ('id', 'email', 'first_name', 'last_name', 'cars', 'password')
```

Similar to the user model, the Car model is related to the UserCar model through a foreign key established in the UserCar model. The LogEntry and Trip models are each related to the UserCar model through a foreign key (see below) which satisfies the many relationship that each have with the UserCar model.

```python
# Foreign Keys
user_car_id = db.Column(
                        db.Integer,
                        db.ForeignKey('user_cars.id', ondelete='cascade'),
                        nullable=False
                    )
```

These established relationships link the LogEntry and Trip models to the User and Car models via the UserCar model. So this means for example, that from a single log entry or user trip object, the user's details can be accessed through the bi-directional relationship established between the User and Usercar. If say the user object was nested in the UserCar model in place of just the user ID, we can see the user's email and name just from accessing a log entry or user trip object. The same goes for the Car model, since it's in the UserCar model as well, a log entry or user trip will be able to show the full details of the car type.

```python
fields = ('id', 'user_id', 'car', 'logs')
```
As seen above, the UserCar schema only exposes the "logs" relationship in the fields and not the "user_trip" relationship that's also defined in the model. This means that even though it's possbile for a user object to access a user trip object thorugh the defined relationships, I have purposely hidden the user trip objects from the user object. So just as you would be able to access user objects from cars, user trips, and log entry objects due to the defined relationships, it's possible to do the opposite. A car object can contain a nested list of all the user objects which contain details of the users, made possible through the UserCar model.


[References](./docs/references.md#r8)

---

## R10 Project Management

Trello was used to track the progress of the API development. The board was organised into 7 different columns, User Stories, Epics, Backlog, Current Sprint, To Do, In Progress, Done. User stories were identified with a pink label, Epics with a purple label and each differentiated from other epics with their own label colour. The tasks were all labelled blue and labelled a second colour relating to their sprint. 

![trello-layout1](./docs/screenshots/trello_fuel_log_1.png)
**Fig. 10**: Trello layout containing Epics, User stories.

- **User Stories**
    - The user stories column contained cards with user stories where the stories were thought of looking from the persepective of potential users. This helped with identifying the scope of the project and keeping track of each story requirement on the board helped to keep the tasks orientated toward completing a user story. Tasks were then created based on the user stories which were tailored accordingly for the appropriate epics.
    - **User Story 1:**
        - The story covers the core feature of what the API is intended for. It identifies that a user should be able to record a log entry for each fill-up. Along with providing insightful information related to fuel costs and usage.
    
    ![user-story-one](./docs/screenshots/user_story.png)
    **Fig. 11**: User Story One.
    - **User Story 2:**
        - The story covers the feature of what the type of report that the API could provide for the user. It identifies that a user should be able to supply a time period and receive a summary for the total fuel cost for the period.
    
    ![user-story-two](./docs/screenshots/user_story2.png)
    **Fig. 12**: User Story Two.
    - **User Story 3:**
        - The story covers the feature that will allow a user to calulate the cost of their trip. It helped identify the key data components that would be needed to create a calculator and this was factored in to the design of the database.
    
    ![user-story-three](./docs/screenshots/user_story3.png)
    **Fig. 13**: User Story Three.
    - **User Story 4:**
        - This story identified the relationship between users and cars. Even though a car comparison was out of scope, the comparision of expenditures for two different periods was determined to be more in scope. 
    
    ![user-story-four](./docs/screenshots/user_story4.png)
    **Fig. 14**: User Story Four.


- **Epics**
    - Epics were used to separate tasks and lay them out to visualise what needed to be done before moving on to the next set of tasks. Each epic contained as many sprints as needed (shown below in Fig. 15) to break down and group the tasks even further to allow a more efficeint build process and direction. The tasks in each sprint for an epic had individual cards created for them and these were added to the Backlog column when an epic was scheduled to be started.
    ![flask-sprints](./docs/screenshots/flask_sprints.png)
    **Fig. 15**: Creating the Flask app and its sprints.
- **Current Sprint**
    - The current sprint contained a card for the sprint that was currently being done. Each sprint had a checklist of the tasks that needed to be done to complete the sprint. And this list was referred to when moving cards from the backlog to the To Do column. 

![trello-layout2](./docs/screenshots/trello_fuel_log_2.png)
**Fig. 18**: Trello layout containing Sprint, To Do, In Progress, Done.

- To Do
    - The To Do column contained every task relating to the current sprint and these cards were moved into the In Progress column as required. The In Progress column didn't have a set limit on the number of tasks that could be placed in it as some tasks in a sprint overlapped with others.
- Done
    - Once a task was done, it was placed into the To Do column and the sprint task list was updated. Once a sprint was done, it was also moved into the column and the Epic containing the sprint was updated.

Another way the project was tracked was through the Daily Standups. This invovled listing what was achieved in a day, identifying any blockers encountered during that period, identifying the goals for the next period, and identifying things learned during the period.

## [Trello Board](https://trello.com/b/IulyjAXj/fuel-log-api)

