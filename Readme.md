Install Docker and give this command "sudo chmod -R 755 ~/.docker"

clone this repository and give the command "docker compose up"


CURD OPERATIONS

curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "email": "testuser@ample.com", "password": "testpassword"}' http://127.0.0.1:8000/inventory_app/register/

curl -X POST -H "Content-Type: application/json" -d '{"email": "testuser@ample.com", "password": "testpassword"}' http://127.0.0.1:8000/inventory_app/login/


With this above command we will get the below output 

```{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyODU4MDIxNCwiaWF0IjoxNzI4NDkzODE0LCJqdGkiOiI2YmU4Yzk3YWVhNmQ0ZmM1YTg3YTVkNDhjYWMxMTliZiIsInVzZXJfaWQiOjF9.ivjUIlw_21Hin54F7Y_B3M_0KMxGsseLfsO-qC56ciE","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NDk0MTE0LCJpYXQiOjE3Mjg0OTM4MTQsImp0aSI6IjQ0MGE5MmIyZDViMTQ1MTM5YjM0NjEyYzhlZTdjNzYyIiwidXNlcl9pZCI6MX0.IwkO1zM22lX3fNwwjcQWZOEJfCBm04pyy0CgkGX2noc"}% ```       

use the access token in the remaininig api calls

curl -X GET -H "Authorization: Bearer Token" http://127.0.0.1:8000/inventory_app/items/

curl -X GET -H "Authorization: Bearer Token" http://127.0.0.1:8000/inventory_app/user/ 

curl -X POST -H "Authorization: Bearer Token" -H "Content-Type: application/json" -d '{"name":"NewItem", "description": "New item description"}' http://127.0.0.1:8000/inventory_app/items/create/

curl -X PUT -H "Authorization: Bearer Token" -H "Content-Type: application/json" -d '{"name": "UpdatedItem", "description": "Updated item description"}' http://127.0.0.1:8000/inventory_app/items/update/1/

curl -X DELETE -H "Authorization: Bearer Token" http://127.0.0.1:8000/inventory_app/items/delete/1/


--------------------
To run the test cases use the below command

docker compose exec django_api pytest -v