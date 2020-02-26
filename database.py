import pymongo as pymongo

client = pymongo.MongoClient("mongodb+srv://admin:SBAadmin@sba-p1w2n.mongodb.net/test?retryWrites=true&w=majority")
db = client.main


Global = db.Global
Locations = db.Locations
Users = db.Users
History = db.History
CustomTables = db.CustomTables

print(db['Global'])


