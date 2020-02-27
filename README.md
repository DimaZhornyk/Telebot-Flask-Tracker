# Telebot-Flask-Tracker
---
### Endpoints:
* #### /login(POST)         example body: {"username": "admin", "password": "admin"}, returns you a JWT token
* #### /location(POST)      example body: {"Name": "home", "Latitude": 22.234455, "Longitude" : 33.445566}:exclamation: requires JWT (creates new location)
* #### /location(DELETE)    example body: {"Name": "home"}:exclamation: requires JWT (deletes location)
* #### /locations(POST) empty body,  returns locations table :exclamation: requires JWT
* #### /history(POST) example body: {"Telegram": 1234567},  returns history of person's recordings to database :exclamation: requires JWT
* #### /update(POST) example body: {"toDelete": [],"toUpdate": [[{"Telegram": 403316002, "Name":"Vaa", "Surname": "Ivanov", "Total time": "23:45:43",Last project":"11", "Last job":"Work"}]]}  :exclamation: requires JWT
* #### /createCustomTable(POST) example body: {"name": "CustomTable1","workers": [[403316002,43253546,45343]]} :exclamation: requires JWT
* #### /customTable(POST) example body: {"name":"CustomTable1"} :exclamation: requires JWT  (returns you a custom table with a given name)
* #### /(GET)        returns index.html
####           (Any other GETs will be redirected to '/')
 
