# ENDPOINTS

All URLs specified point to the Localhost server at the default port 5000 when the Flask API is run.


## <a name="head1"></a> POST    /login

Let's the user authenticate and recieve an access token

##### Resource Information

|  | |
| ------ | ----- |
| Method | POST |
| URL | http://127.0.0.1:5000/login |
| Requires authentication | No |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| email | (string) | The email of the user  |
| password | (string) | The password of the user |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| token | (string) | The token generated once the user is authenticated  |
| user | (object) | Details of the athenticated user |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |
| 400 | bad_request | No JSON object Found in request body |
| 401 | invalid_user_info | Invalid email address or password |


##### Example

###### Request

```
{
    "email": "will.thomas@gmail.com",
    "password": "thisIsapassword"
}
```

###### Response

```
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4Nzc4MTg0MSwianRpIjoiZTBmMWQwODItYTAwMS00OWJlLTg2NDAtZGY0ODQwNDc2OTE3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNjg3NzgxODQxLCJleHAiOjE2ODc3ODkwNDF9.9-xFSzsr7K0mSvdu7Rz__Fvf17Pu2NhuNyup0s9zdY4",
    "user": {
        "email": "will.thomas@gmail.com",
        "first_name": "William",
        "last_name": "Thomas",
        "cars": [
            {
                "car": {
                    "make": "Ford",
                    "model": "Ranger",
                    "model_trim": "Raptor",
                    "year": 2022,
                }
            }
        ]
    }
}
```

[Back to Main](../README.md#user-access-and-account-management)

## <a name="head2"></a> POST    /register

Let's a user register to use the API.

##### Resource Information

|  | |
| ------ | ----- |
| Method | POST |
| URL | http://127.0.0.1:5000/register |
| Requires authentication | No |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| email | (string) | The email of the new user  |
| password | (string) | The password of the new user |
| first_name | (string) | Optional: The firstname of the new user |
| last_name | (string) | Optional: The lastname of the new user |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| msg | (string) | A message to indicate successful registration  |
| user_info | (object) | Details of the registered user |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |
| 400 | bad_request | No JSON object Found in request body |

##### Example

###### Request

```
{
    "email": "john.smith@gmail.com",
    "password": "password123",
    "first_name": "John"
}
```

###### Response

```
{
    "msg": "Successfully created new user",
    "user_info": {
        "id": 4,
        "email": "john.smith@gmail.com",
        "first_name": "John",
        "last_name": "null",
        "cars": []
    }
}
```

[Back to Main](../README.md#user-access-and-account-management)

## <a name="head3"></a> DELETE    /me/$user_id/delete/

Allows a user to delete their account. Admin accessing this endpoint can delete any user.

##### Resource Information

|  | |
| ------ | ----- |
| Method | DELETE |
| URL | http://127.0.0.1:5000/me/$user_id/delete/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $user_id | (int) | User ID |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| deleted | (string) | A message to indicate successful deletion of user record by user |
| admin_deleted | (string) | A message to indicate successful deletion of user record by admin |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 401 | unauthorized | Admin access only |
| 403 | forbidden | You must be logged in or registered |
| 404 | invalid_user | User not found |

##### Example

###### Request

ADMIN Delete

```
http://127.0.0.1:5000/me/3/delete/
```

###### Response

```
{
    "admin_deleted": "user successfully deleted"
}
```

[Back to Main](../README.md#user-access-and-account-management)

## <a name="head4"></a> GET  /cars/

Get a list of all cars.

##### Resource Information

|  | |
| ------ | ----- |
| Method | GET |
| URL | http://127.0.0.1:5000/cars/ |
| Requires authentication | Yes |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| List | (object) | A list containing objects of all cars |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |

##### Example

###### Request

```
http://127.0.0.1:5000/cars/
```

###### Response

```
[
    {
        "id": 1,
        "make": "Ford",
        "model": "Ranger",
        "model_trim": "Raptor",
        "year": 2022,
        "tank_size": 80
    },
    {
        "id": 2,
        "make": "Toyota",
        "model": "Landcruiser",
        "model_trim": "100 series",
        "year": 2004,
        "tank_size": 110
    },
    {
        "id": 3,
        "make": "Ford",
        "model": "Focus",
        "model_trim": "Trend",
        "year": 2013,
        "tank_size": 50
    }
]
```

[Back to Main](../README.md#cars)

## <a name="head5"></a> GET  /cars/$make/

Get a filtered list of cars by make.

##### Resource Information

|  | |
| ------ | ----- |
| Method | GET |
| URL | http://127.0.0.1:5000/cars/$make/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $make | (string) | Make name |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| List | (object) | A list containing objects of all cars by make |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | Car make not found |

##### Example

###### Request

```
http://127.0.0.1:5000/cars/ford/
```

###### Response

```
[
    {
        "id": 1,
        "make": "Ford",
        "model": "Ranger",
        "model_trim": "Raptor",
        "year": 2022,
        "tank_size": 80
    },
    {
        "id": 3,
        "make": "Ford",
        "model": "Focus",
        "model_trim": "Trend",
        "year": 2013,
        "tank_size": 50
    }
]
```

[Back to Main](../README.md#cars)

## <a name="head6"></a> GET  /cars/$make/\$model

Get a filtered list of cars by make and model.

##### Resource Information

|  | |
| ------ | ----- |
| Method | GET |
| URL | http://127.0.0.1:5000/cars/$make/\$model |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $make | (string) | Make name |
| $model| (string) | Model name |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| List | (object) | A list containing objects of all cars by make and model |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | Car make or model not found |

##### Example

###### Request

```
http://127.0.0.1:5000/cars/ford/ranger
```

###### Response

```
[
    {
        "id": 1,
        "make": "Ford",
        "model": "Ranger",
        "model_trim": "Raptor",
        "year": 2022,
        "tank_size": 80
    }
]
```

[Back to Main](../README.md#cars)

## <a name="head7"></a> GET  /cars/me/

Get a list of all cars that belong to the authenticated user.

##### Resource Information

|  | |
| ------ | ----- |
| Method | GET |
| URL | http://127.0.0.1:5000/cars/me/ |
| Requires authentication | Yes |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| List | (object) | A list containing objects of all user cars |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | User has no cars added to their list |


##### Example

###### Request

```
http://127.0.0.1:5000/cars/me/
```

###### Response

```
[
    {
        "id": 1,
        "make": "Ford",
        "model": "Ranger",
        "model_trim": "Raptor",
        "year": 2022,
        "tank_size": 80
    },
]
```

[Back to Main](../README.md#cars)

## <a name="head8"></a> POST  /cars/me/

Add a new car to the user's car list. The car is also added to the cars list.

##### Resource Information

|  | |
| ------ | ----- |
| Method | POST |
| URL | http://127.0.0.1:5000/cars/me/ |
| Requires authentication | Yes |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| make | (string) | The make of the car  |
| model | (string) | The model of the car|
| model_trim | (string) | The model trim of the car|
| year | (int) | The year of manufacture for the car|
| tank_size | (int) | The tank size of the car|

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| id | (int) | The ID of the user car |
| car | (object) | An object containing the information of the car |
| logs | (object) | An Empty list of the user car's log |


##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 400 | integrity_error | Data already exists in database |
| 400 | bad_request | No JSON object Found in request body |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |
| 403 | forbidden | You must be logged in or registered |



##### Example

###### Request

```
{
    "make": "Ford",
    "model": "Focus",
    "model_trim": "Trend",
    "year": 2013,
    "tank_size": 50
}
```

###### Response

```
{
    "id": 4,
    "car": {
        "id": 10,
        "make": "Ford",
        "model": "Focus",
        "model_trim": "Trend",
        "year": 2013,
        "tank_size": 50
    },
    "logs": []
}
```

[Back to Main](../README.md#cars)

## <a name="head9"></a> DELETE  /cars/me/$user_car_id

Delete a car in user's car list.

##### Resource Information

|  | |
| ------ | ----- |
| Method | DELETE |
| URL | http://127.0.0.1:5000/cars/me/$user_car_id |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $user_car_id | (int) | The ID of the user's car in the user's list |


##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| deleted | (string) | A message confirming the successful deletion of the user car |


##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 404 | not_found | User car not found |




##### Example

###### Request

```
http://127.0.0.1:5000/cars/me/
```

###### Response

```
{
    "deleted": "removed car from user list"
}
```

[Back to Main](../README.md#cars)

## <a name="head10"></a> DELETE  /cars/$car_id

ADMIN ONLY: Admin can delete a car which will delete from all user car lists.

##### Resource Information

|  | |
| ------ | ----- |
| Method | DELETE |
| URL | http://127.0.0.1:5000/cars/$car_id |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the cars list |


##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| admin_deleted | (string) | A message confirming the successful deletion of the car by the admin.|


##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 401 | unauthorized | Admin access only |
| 404 | not_found | Car not found |

##### Example

###### Request

```
http://127.0.0.1:5000/cars/3
```

###### Response

```
{
    "admin_deleted": "car successfully deleted"
}
```

[Back to Main](../README.md#cars)

## <a name="head11"></a> PUT/PATCH  /cars/$car_id

ADMIN ONLY: Admin can delete a car which will delete from all user car lists.

##### Resource Information

|  | |
| ------ | ----- |
| Methods | PUT, PATCH |
| URL | http://127.0.0.1:5000/cars/$car_id |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the cars list |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| make | (string) | The make of the car  |
| model | (string) | The model of the car|
| model_trim | (string) | The model trim of the car|
| year | (int) | The year of manufacture for the car|
| tank_size | (int) | The tank size of the car|

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| id | (int) | The ID of the car  |
| make | (string) | The make of the car  |
| model | (string) | The model of the car|
| model_trim | (string) | The model trim of the car|
| year | (int) | The year of manufacture for the car|
| tank_size | (int) | The tank size of the car|


##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |
| 400 | bad_request | No JSON object Found in request body |
| 401 | unauthorized | Admin access only |
| 404 | not_found | Car not found |

##### Example

###### Request

```
{
    "make": "Ford",
    "model": "Focus",
    "model_trim": "Trend",
    "year": 2013,
    "tank_size": "80"
}
```

###### Response

```
{
    "id": 3,
    "make": "Ford",
    "model": "Focus",
    "model_trim": "Trend",
    "year": 2013,
    "tank_size": 80
}
```

[Back to Main](../README.md#cars)

## <a name="head12"></a> GET  /logs/me/$car_id/

Get a list of the logs that belong to the authenticated user's car.

##### Resource Information

|  | |
| ------ | ----- |
| Method | GET |
| URL | http://127.0.0.1:5000/logs/me/$car_id/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| List | (object) | A list containing Dict objects of all the logs of the user's car |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | No log entries for user car |
| 404 | not_found | User car not found |

##### Example

###### Request

```
http://127.0.0.1:5000/logs/me/2/
```

###### Response

```
[
    {
        "id": 1,
        "current_odo": 80100,
        "fuel_quantity": 80,
        "fuel_price": 1.86,
        "date_added": 1687764209,
        "usercar": {
            "id": 2,
            "user_id": 3,
            "car": {
                "id": 1,
                "make": "Ford",
                "model": "Ranger",
                "model_trim": "Raptor",
                "year": 2022,
                "tank_size": 80
            }
        }
    },
    {
        "id": 3,
        "current_odo": 80700,
        "fuel_quantity": 80,
        "fuel_price": 1.92,
        "date_added": 1687781965,
        "usercar": {
            "id": 2,
            "user_id": 3,
            "car": {
                "id": 1,
                "make": "Ford",
                "model": "Ranger",
                "model_trim": "Raptor",
                "year": 2022,
                "tank_size": 80
            }
        }
    },
    {
        "id": 4,
        "current_odo": 81200,
        "fuel_quantity": 60,
        "fuel_price": 1.92,
        "date_added": 1687781985,
        "usercar": {
            "id": 2,
            "user_id": 3,
            "car": {
                "id": 1,
                "make": "Ford",
                "model": "Ranger",
                "model_trim": "Raptor",
                "year": 2022,
                "tank_size": 80
            }
        }
    },
]
```

[Back to Main](../README.md#logs)

## <a name="head13"></a> POST  /logs/me/$car_id/

Add a new log entry for the authenticated user's car.

##### Resource Information

|  | |
| ------ | ----- |
| Method | POST |
| URL | http://127.0.0.1:5000/logs/me/$car_id/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| current_odo | (int) | The current odometer reading of the car  |
| fuel_quantity | (int) | The amount of fuel added to the car|
| fuel_price | (float) | The price of fuel added|

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| id | (int) | The ID of the log entry  |
| current_odo | (int) | The current odometer reading of the car  |
| fuel_quantity | (int) | The amount of fuel added to the car|
| fuel_price | (float) | The price of fuel added|
| date_added | (bigint) | The date added for the log entry (Datetime timestamp format)  |
| usercar | (object) | An object containing the user car information|

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |
| 400 | bad_request | No JSON object Found in request body |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | User car not found |

##### Example

###### Request

```
{
    "current_odo": 81800,
    "fuel_quantity": 75,
    "fuel_price": 1.92
}
```

###### Response

```
{
    "id": 6,
    "current_odo": 81800,
    "fuel_quantity": 75,
    "fuel_price": 1.92,
    "date_added": 1687846764,
    "usercar": {
        "id": 2,
        "user_id": 3,
        "car": {
            "id": 1,
            "make": "Ford",
            "model": "Ranger",
            "model_trim": "Raptor",
            "year": 2022,
            "tank_size": 80
        }
    }
}
```

[Back to Main](../README.md#logs)

## <a name="head14"></a> PUT/PATCH  /logs/me/$car_id/\$log_id/

Update a log entry for the authenticated user's car.

##### Resource Information

|  | |
| ------ | ----- |
| Methods | PUT, PATCH |
| URL | http://127.0.0.1:5000/logs/me/$car_id/\$log_id/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |
| $log_id | (int) | The ID of the log entry in the user's car log list |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| current_odo | (int) | The current odometer reading of the car  |
| fuel_quantity | (int) | The amount of fuel added to the car|
| fuel_price | (float) | The price of fuel added|

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| id | (int) | The ID of the log entry  |
| current_odo | (int) | The current odometer reading of the car  |
| fuel_quantity | (int) | The amount of fuel added to the car|
| fuel_price | (float) | The price of fuel added|
| date_added | (bigint) | The date added for the log entry (Datetime timestamp format)  |
| usercar | (object) | An object containing the user car information|

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |
| 400 | bad_request | No JSON object Found in request body |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | Log entry not found |
| 404 | not_found | User car not found |

##### Example

###### Request

```
{
    "current_odo": 81800,
    "fuel_quantity": 75,
    "fuel_price": 1.92
}
```

###### Response

```
{
    "id": 6,
    "current_odo": 81800,
    "fuel_quantity": 75,
    "fuel_price": 1.92,
    "date_added": 1687846764,
    "usercar": {
        "id": 2,
        "user_id": 3,
        "car": {
            "id": 1,
            "make": "Ford",
            "model": "Ranger",
            "model_trim": "Raptor",
            "year": 2022,
            "tank_size": 80
        }
    }
}
```

[Back to Main](../README.md#logs)

## <a name="head15"></a> DELETE  /logs/me/$car_id/\$log_id/

Update a log entry for the authenticated user's car.

##### Resource Information

|  | |
| ------ | ----- |
| Method | DELETE |
| URL | http://127.0.0.1:5000/logs/me/$car_id/\$log_id |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |
| $log_id | (int) | The ID of the log entry in the user's car log list |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| deleted | (string) | A message confirming the successful deletion of the user car's log entry  |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | Log entry not found |
| 404 | not_found | User car not found |

##### Example

###### Request

```
http://127.0.0.1:5000/logs/me/2/6
```

###### Response

```
{
    "deleted" : "Log entry deleted from user car"
}
```

[Back to Main](../README.md#logs)

## <a name="head16"></a> POST  /logs/me/$car_id/trip/calculator/

The calculator takes a distance and current fuel price. Calculates how much a trip will cost using the average consumption which is calculated from the user's car logs

##### Resource Information

|  | |
| ------ | ----- |
| Method | POST |
| URL | http://127.0.0.1:5000/logs/me/$car_id/trip/calculator/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| distance | (int) | The trip distance  |
| fuel_price | (float) | The current price of fuel|

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| avg_consumption | (string) | The average fuel consumption of the user's car  |
| estimated_trip_fuel | (string) | The estimated fuel needed for the trip  |
| esitmated_trip_cost | (string) | The estimated cost of fuel for the trip|
| car | (object) | An object contains infomation on the user's car |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |
| 400 | bad_request | No JSON object Found in request body |
| 400 | calc_error | Unable to calc average consumption due to num of log entries present |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | User car not found |

##### Example

###### Request

```
{
    "distance": 100,
    "fuel_price": 1.92
}
```

###### Response

```
{
    "avg_consumption": "12.73 L/100km",
    "estimated_trip_fuel": "12.73 L",
    "esitmated_trip_cost": "$24.44",
    "car": {
        "make": "Ford",
        "model": "Ranger",
        "model_trim": "Raptor",
        "year": 2022,
    }
}
```

[Back to Main](../README.md#logs)

## <a name="head17"></a> GET  /logs/me/$car_id/trips/

Get all trips for the authenticated user's car.

##### Resource Information

|  | |
| ------ | ----- |
| Method | GET |
| URL | http://127.0.0.1:5000/logs/me/$car_id/trips/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| List | (object) | A List containing Dict object with trip details  |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | User car not found |
| 404 | not_found | User car has no trips |

##### Example

###### Request

```
http://127.0.0.1:5000/logs/me/2/trips/
```

###### Response

```
[
    {
        "id": 2,
        "fuel_price": 1.9,
        "distance": 400,
        "user_car_id": 2
    },
    {
        "id": 3,
        "fuel_price": 1.95,
        "distance": 800,
        "user_car_id": 2
    },
    {
        "id": 4,
        "fuel_price": 1.92,
        "distance": 100,
        "user_car_id": 2
    }
]
```

[Back to Main](../README.md#logs)

## <a name="head18"></a> DELETE  /logs/me/$car_id/trips/\$trip_id

Delete a trip for the authenticated user's car.

##### Resource Information

|  | |
| ------ | ----- |
| Method | DELETE |
| URL | http://127.0.0.1:5000/logs/me/$car_id/trips/\$trip_id |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |
| $trip_id | (int) | The ID of trip in the user's car trip list |

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| delete | (string) | A message confirming the successful deletion of the user car's trip  |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | User car not found |
| 404 | not_found | User car trip does not exsist |

##### Example

###### Request

```
http://127.0.0.1:5000/logs/me/2/trips/3
```

###### Response

```
{
    "deleted" : "Trip successfully deleted"
}
```

[Back to Main](../README.md#logs)

## <a name="head19"></a> PUT/PATCH  /logs/me/$car_id/trips/\$trip_id

Update a trip for the authenticated user's car.

##### Resource Information

|  | |
| ------ | ----- |
| Methods | PUT, PATCH |
| URL | http://127.0.0.1:5000/logs/me/$car_id/trips/\$trip_id |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |
| $trip_id | (int) | The ID of trip in the user's car trip list |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| distance | (int) | The trip distance  |
| fuel_price | (float) | The current price of fuel|

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| id | (int) | The trip ID for the user's car  |
| fuel_price | (float) | The fuel price at the time of the trip  |
| distance | (int) | The trip distance for the user's car  |
| user_car_id | (int) | The ID for the user's car  |


##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |
| 400 | bad_request | No JSON object Found in request body |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | User car not found |
| 404 | not_found | User car trip does not exsist |

##### Example

###### Request

```
{
    "distance": 800,
    "fuel_price": 1.95
}
```

###### Response

```
{
    "id": 3,
    "fuel_price": 1.95,
    "distance": 800,
    "user_car_id": 2
}
```

[Back to Main](../README.md#logs)

## <a name="head20"></a> POST  /logs/me/\$car_id/expenditure/

Get an expenditure summary for a specified time period for the authenticated user's car. The endpoint takes a "to_date" and "from_date" dates in the request body. 

**Date format in request:** "YYYY-mm-dd"

##### Resource Information

|  | |
| ------ | ----- |
| Method | POST |
| URL | http://127.0.0.1:5000/logs/me/\$car_id/expenditure/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| to_date | (date) | The date ending  |
| from_date | (date) | The date starting|

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| from | (string) | The "from" date  |
| to | (string) | The "to" date  |
| total_cost_for_period | (string) | The total cost for the specified period for the user's car  |
| total_distance_for_period | (string) | The total distance travelled for the specified period for the user's car  |


##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | User car not found |
| 404 | not_found | No expenditure for period specified |

##### Example

###### Request

```
{
    "from_date": "2023-6-1",
    "to_date": "2023-6-29"
}
```

###### Response

```
{
    "from": "2023-06-1",
    "to": "2023-06-29",
    "total_cost_for_period": "$561.60",
    "total_distance_for_period": "1700 km"
    "user_car": {
        "car": {
            "make": "Ford",
            "model": "Ranger",
            "model_trim": "Raptor",
            "year": 2022
        }
    }
}
```

[Back to Main](../README.md#logs)

## <a name="head21"></a> POST  /logs/me/\$car_id/expenditure/compare/

Compare expenditure summaries for specified time periods for the authenticated user's car. The endpoint takes a "to_date" and "compare_from_date" and "compare_to_date" and "from_date" dates in the request body. 

**Date format in request:** "YYYY-mm-dd"

##### Resource Information

|  | |
| ------ | ----- |
| Method | POST |
| URL | http://127.0.0.1:5000/logs/me/\$car_id/expenditure/compare/ |
| Requires authentication | Yes |

##### Method Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| $car_id | (int) | The ID of the car in the user's car list |

##### Request Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| to_date | (date) | The date ending  |
| from_date | (date) | The date starting|
| compare_to_date | (date) | The date ending for the comparison period |
| compare_from_date | (date) | The date starting for the comparison period|

##### Response Parameters

| Parameter | Type | Description |
| ------ | ----- | ----- |
| period_one | (object) | Period one summmary  |
| period_two | (object) | Period two summary |


##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 403 | forbidden | You must be logged in or registered |
| 404 | not_found | User car not found |
| 404 | not_found | No expenditure for period specified |

##### Example

###### Request

```
{
    "from_date": "2023-6-1",
    "to_date": "2023-6-29",
    "compare_from_date": "2023-5-1",
    "compare_to_date": "2023-5-31"
}
```

###### Response

```
{
    "period_one": {
        "expenditure_summary_for": {
            "to_date": "2023-06-29",
            "from_date": "2023-06-01"
        },
        "total_cost_for_period": "$270.00",
        "total_distance_for_period": "700 km",
        "user_car": {
            "car": {
                "make": "Ford",
                "model": "Ranger",
                "model_trim": "Raptor",
                "year": 2022
            }
        }
    },
    "period_two": {
        "expenditure_summary_for": {
            "compare_to_date": "2023-05-31",
            "compare_from_date": "2023-05-01"
        },
        "total_cost_for_period": "$528.80",
        "total_distance_for_period": "1800 km",
        "user_car": {
            "car": {
                "make": "Ford",
                "model": "Ranger",
                "model_trim": "Raptor",
                "year": 2022
            }
        }
    }
}
```

[Back to Main](../README.md#logs)