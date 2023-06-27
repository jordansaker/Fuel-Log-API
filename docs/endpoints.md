# ENDPOINTS

All URLs specified point to the Localhost server at the default port 5000 when the Flask API is run.

## POST    /login

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
| user | (dict) | Details of the athenticated user |

##### Resource Errors

These are the possible errors returned by the endpoint.

| HTTP Code | Error Identifier | Error Message |
| ------ | ----- | ----- |
| 401 | invalid_user_info | Invalid email address or password |
| 400 | valiadtion_error | Returns a dict with the keys that fail the validation |

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
                    "id": 1,
                    "make": "Ford",
                    "model": "Ranger",
                    "model_trim": "Raptor",
                    "year": 2022,
                    "tank_size": 80
                }
            }
        ]
    }
}
```

[Back to Main](../README.md#user-access-and-account-management)