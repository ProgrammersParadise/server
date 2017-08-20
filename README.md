# server

## required packages
The following python packages are required to run the backend services:
- cherrypy (>=3.8.0)
- sqlalchemy (>=1.0.17; with psycopg2 for postgres or pymysql for mysql)
- bcrypt (>=3.1.1)
- requests (>=2.11.x)

## setup
Create one database user and database for the auth backend and another for the content backend. Each of the two servers (auth and content) has its own `config.ini`, where user, password and database information needs to be configured.

After both have been configured, run `./main.py` in both auth and content directories.

## creating a demo user
To create a demo user you can use the commandline tool curl.
```
$> curl -X PUT -F username=MYUSER -F password=MYPASSWORD http://localhost:14001/user
OK
```
It should reply with a `OK`.

To receive a temporary auth token for debugging, just send a POST request to `/auth`:
```
$> curl -X POST -F username=MYUSER -F password=MYPASSWORD http://localhost:14001/auth
{"token": "MYTOKEN", "expires": "2017-08-20 20:56:51.463933"}
```
To validate this token send a POST request to `/login`:
```
$> curl -X POST -F token=MYTOKEN http://localhost:14001/login
{"userid": 1}
```
Clients will not be able to talk with the auth service on port 14001, but can talk with the content service on port 14002. The login can be done like this:
```
$> curl -X POST -F username=MYUSER -F password=MYPASSWORD http://localhost:14002/login
{"token": "MYTOKEN", "expires": "2017-08-20 21:01:00.982042"}
```
Now with that access token, data can be requested from the server, which is not implemented further yet:
```
$> curl -H 'Authorization: Token MYTOKEN' http://localhost:14002/category
Success! Sadly this is not implemented yet, but your internal userid is 1
```

