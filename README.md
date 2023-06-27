# Fuel Log API

#### Installation

Requirements:
- PostgreSQL    :       "psql"
- Python 3         :        (Python 3.11.3 used)

##### Database setup






## REST API Resources

A full listing of all available endpoints can be found [here](./docs/endpoints.md).

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
|[GET               /cars/$make/](./docs/endpoints.md#head5) | Get a list of all cars by make.|
|[GET               /cars/$make/\$model](./docs/endpoints.md#head6) | Get a list of all cars by make and model.|
|[GET               /cars/me/](./docs/endpoints.md#head7) | Get the list of cars belonging to the user.|
|[POST             /cars/me/](./docs/endpoints.md#head8) | Add a car to the user's list of cars.|
|[DELETE         /cars/me/$user_car_id](./docs/endpoints.md#head9) | Delete a car from the user's car list.|
|[DELETE         /cars/$car_id](./docs/endpoints.md#head10) | ADMIN ONLY:  Delete a car from the car index.|
|[PUT/PATCH   /cars/$car_id](./docs/endpoints.md#head11) | ADMIN ONLY:  Update a car's details.|

#### Logs

| Resource | Description |
| --------------------- | ---------- |
|[GET                 /logs/me/$car_id/](./docs/endpoints.md#head12) | Get the user's logs for the selected car. |
|[POST              /logs/me/$car_id/](./docs/endpoints.md#head13) | Add a new log for the selected user car. |
|[PUT/PATCH    /logs/me/$car_id/\$log_id/](./docs/endpoints.md#head14) | Update a log for the selected user car. |
|[DELETE          /logs/me/$car_id/\$log_id](./docs/endpoints.md#head15) | Delete a log for the selected user car. |
|[POST              /logs/me/$car_id/trip/calculator/](./docs/endpoints.md#head16) | Calculate the total fuel cost of a trip. |
|[GET                 /logs/me/$car_id/trips/](./docs/endpoints.md#head17) | Get the user car's list of trips. |
|[DELETE           /logs/me/$car_id/trips/\$trip_id](./docs/endpoints.md#head18) | Delete a trip for the selected user car. |
|[PUT/PATCH    /logs/me/$car_id/trips/\$trip_id](./docs/endpoints.md#head19) | Update the trip details for the selected user car. |
|[GET                /logs/me/$car_id/expenditure/from/\$from_day/\$from_month/\$from_year/to/\$to_day/\$to_month/\$to_year/](./docs/endpoints.md#head20) | Get the expenditure summary for a time period |

#### The problem this API app is trying to solve

With fuel prices rising steadily over the last 5 years, more car owners are looking for ways to keep running costs down. This application will provide a way for users to track their fuel consuption from bowser to bowser, while providing multiple forecasts and estimations based on their fuel consumption and current fuel costs at the bowsers which will be useful for budgeting purposes.

- The app will help the user budget and plan ahead for fuel expenses for the month
    - It will return the total cost of fuel for a time period and the total distance travelled within that timeframe.
- The user can calculate the esitmated cost of a trip by providing the distance and the price of fuel
- The average consumption per 100 km is returned each time the user calculates the cost of a trip. This consumption rate is used to estimate the total cost of the trip.
- It allows users to add multiple cars to their list to track separately.

## ERD

![Fuel log API ERD](./docs/ERD.png)

#### Entities

- Users
- Log Entries
- Cars
- User Cars
- Trips

## Third Party Services

pip install flask, flask-sqlalchemy, flask-bcrypt, flask-marshmallow, psycopg2-binary, flask-JWT-Extended, orjson marshmallow-sqlalchemy, python-dotenv
