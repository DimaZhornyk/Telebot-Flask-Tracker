import pymongo as pymongo

client = pymongo.MongoClient("databseURL")
db = client.main


Workers = db.Workers
Locations = db.Locations
Users = db.Users
History = db.History
CustomTables = db.CustomTables
Metadata = db.Metadata



