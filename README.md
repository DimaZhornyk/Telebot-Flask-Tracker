# Telebot-Flask-Tracker
---
### Endpoints:
* #### /login(POST)         example body: {"username": "admin", "password": "admin"}, returns you a JWT token
* #### /location(POST)      example body: {"name": "home", "lat": 22.234455, "lng" : 33.445566}:exclamation: requires JWT (creates new location)
* #### /location(DELETE)    example body: {"name": "home"}:exclamation: requires JWT (deletes location)
* #### /locations(POST) empty body,  returns locations table :exclamation: requires JWT
* #### /history(POST) example body: {"id": 1234567},  returns history of person's recordings to database :exclamation: requires JWT
* #### /update(POST) example body: {"toDelete": [],"toUpdate": [[{"id": 403316002}, {"name":"Vasya"}, {"surname": "Ivanov"}, {"total_hours": 123}, {"total_minutes": 23}, {"total_seconds":44}, {"last_project":"11"}, {"last_job":"Work"},{"lastLat":123.5556}, {"lastLng":45.56666},{"project_chosen":"11"}]]}  :exclamation: requires JWT
* #### /(GET)        returns main page with table :exclamation: requires JWT
####           (Any other GETs will be redirected to '/')
 
