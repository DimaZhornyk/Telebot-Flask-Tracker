# Telebot-Flask-Tracker
---
### Endpoints:
* #### /login(POST)         example body: {"username": "admin", "password": "admin"}, returns you a JWT token
* #### /location(POST)      example body: {"name": "home", "lat": 22.234455, "lng" : 33.445566}:exclamation: requires JWT (creates new location)
* #### /location(DELETE)    example body: {"name": "home"}:exclamation: requires JWT (deletes location)
* #### /worker(DELETE)      example body: {"name": "Vasya", "surname": "Voylov"}:exclamation: requires JWT (deletes a worker from a global table)
* #### /(GET)        returns main page with table
* #### /locations(GET) returns locations table
#### (Any other GETs will be redirected to '/')
 
