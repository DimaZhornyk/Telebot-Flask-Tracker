import pymongo as pymongo

client = pymongo.MongoClient("mongodb+srv://admin:SBAadmin@sba-p1w2n.mongodb.net/test?retryWrites=true&w=majority")
db = client.main


Workers = db.Workers
Locations = db.Locations
Users = db.Users
History = db.History
CustomTables = db.CustomTables
Metadata = db.Metadata



