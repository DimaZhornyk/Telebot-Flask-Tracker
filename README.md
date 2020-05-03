# Telebot-Flask-Tracker (Flask, Mongo, Svelte, Telebot)
---
## Endpoints:
* ### /login(POST)         example body: {"username": "admin", "password": "admin"}, returns you a JWT token
* ### /requiredFields(POST)      empty body:exclamation: requires JWT (returns a list of fields required to create an own table)
* ### /tables(POST) example body: {"Name": "History"}, :exclamation: requires JWT, return a named table or errro if table not found
* ### /tables(PATCH) example body: {"tableName": "Locations","rowsToEdit": [],"rowsToDelete": [],"rowsToAdd": [[{"Name": "Teremky", "Latitude": 50.370042, "Longitude":30.456304}]]}  :exclamation: requires JWT, !!!BE VERY CAREFUL WITH SQUARE BRACKETS
* ### /tables(PUT) example body: {"Name": "My custom table","keys": [["Telegram","Name", "Surname","Total time", "Last project", "Last job", "Phone", "E-mail"]]} :exclamation: requires JWT, creates a table with a given parameters, mind that they have to satisfy requiredFields
* ### /tables(DELETE) example body: {"Name": "History"}, :exclamation: requires JWT , deletes table
* ### /(GET)        returns index.html
####           (Any other GETs will be redirected to '/')
 
