from bson import ObjectId
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, request
from database import db, Locations


class Tables(Resource):
    # to find table by name
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        if db[data['Name']]:  # if table exists
            table = db[data['Name']].find()  # taking the table
            metadata = db['Metadata'].find_one({"Name": data['Name']})
            allowed_keys = metadata["keys"]  # taking the keys to return from table
            to_return = []
            for el in table:  # checking each table line and taking the needed elements
                res = {}
                for el_key in el.keys():
                    if el_key in allowed_keys:
                        res[el_key] = el[el_key]
                try:
                    if res['Last project']:
                        res['Last project'] = Locations.find_one({"_id": res["Last project"]})['Name']
                except:
                    if 'Last project' in res:
                        if isinstance(res['Last project'], ObjectId):
                            res['Last project'] = 'unknown'
                to_return.insert(0, res)
            metadata.pop('_id', None)
            return {"table": to_return, "metadata": metadata}
        return {"message": "Table not found"}

    # to edit an existing table
    @jwt_required
    def patch(self):
        try:
            data = request.get_json(force=True)
        except:
            return {}, 400
        try:
            allowed_keys = db['Metadata'].find_one({"Name": data['tableName']})["keys"]
        except:
            return {}, 400
        table_name = data['tableName']
        rows_to_edit = data['rowsToEdit']
        rows_to_add = data['rowsToAdd']
        rows_to_delete = data['rowsToDelete']
        for row in rows_to_edit:
            new_values = {}
            for key in row.keys():
                if key in allowed_keys:
                    new_values[key] = row[key]
            if db['Metadata'].find_one({"Name": data['tableName']})["containsWorkers"]:
                query = {'Telegram': row['Telegram']}
            elif db['Metadata'].find_one({"Name": data['tableName']})["containsGeo"]:
                query = {'ID': row['ID']}
            else:
                query = {'Time': row['Time']}
            db[table_name].update_one(query, {'$set': new_values})
        # if we are deleting people, telegrams have to be in data, if locations - IDs

        for index in rows_to_delete:
            if db['Metadata'].find_one({"Name": table_name})["containsWorkers"]:
                query = {'Telegram': index}
            elif db['Metadata'].find_one({"Name": table_name})["containsGeo"]:
                query = {'ID': int(index)}
            else:
                return {}, 400
            db[table_name].delete_one(query)

        if len(rows_to_add) > 0:
            if db['Metadata'].find_one({"Name": table_name})["containsWorkers"]:
                workers = True
            elif db['Metadata'].find_one({"Name": table_name})["containsGeo"]:
                workers = False
            else:
                return {}, 400

        for row in rows_to_add:
            new_value = {}
            for key in row.keys():
                if key in allowed_keys:
                    new_value[key] = row[key]
            if not workers:
                new_value['ID'] = get_sequence('loc')
            if workers is False and db[table_name].find_one({"Name": row["Name"]}) is None:
                db[table_name].insert_one(new_value)
            elif workers and db[table_name].find_one({"Telegram": row["Telegram"]}) is None:
                db[table_name].insert_one(new_value)
        return {"message": "Successfully done"}, 200

    # to create a new table
    @jwt_required
    def put(self):
        data = request.get_json(force=True)
        keys = data["keys"]
        for key in db["Metadata"].find_one({"Name": "Required fields"})["keys"]:
            if key not in keys:
                return {"message": "Not all required keys specified"}, 400
        if data["Name"] in db.list_collection_names():
            return {"message": "Table with this name already exists"}, 400
        collection = db[data["Name"]]
        collection.insert_one({"Initial": "Initial"})
        collection.delete_one({"Initial": "Initial"})
        db["Metadata"].insert_one(
            {"Name": data["Name"],
             "keys": keys,
             "containsWorkers": True,
             "containsGeo": False})
        return {"message": "Collection successfully created"}

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Name", type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        table_name = data['Name']
        try:
            db[table_name].drop()
            db['Metadata'].delete_one({"Name": data["Name"]})
            return {"message": "Successfully deleted"}
        except:
            return {}, 400


class Worker(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Telegram", type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        try:
            workers = list(db['History'].find({"Telegram": int(data['Telegram'])}))
            for worker in workers:
                worker.pop('_id')
            return list(reversed(workers))
        except:
            return {}, 400


def get_sequence(name):
    collection = db.sequences
    document = collection.find_one_and_update({"_id": name}, {"$inc": {"value": 1}}, return_document=True)
    return document["value"]
