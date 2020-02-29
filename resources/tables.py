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
            metadata = db['Metadata'].find_one({"Name": data['Name']});
            allowed_keys = metadata["keys"]  # taking the keys to return from table
            to_return = []
            for el in table:  # checking each table line and taking the needed elements
                res = {}
                for el_key in el.keys():
                    if el_key in allowed_keys:
                        res[el_key] = el[el_key]
                try:
                    if res['Last project']:
                        res['Last project'] = Locations.find_one({"_id": el["Last project"]})['Name']
                except:
                    pass
                to_return.append(res)
                metadata.pop('_id', None)
            return {"table": to_return, "metadata": metadata}
        return {"message": "Table not found"}

    # to edit an existing table
    @jwt_required
    def patch(self):
        data = request.get_json(force=True)
        try:
            allowed_keys = db['Metadata'].find_one({"Name": data['tableName']})["keys"]
        except:
            return {"message": "An error occurred"}
        table_name = data['tableName']
        rows_to_edit = data['rowsToEdit']
        rows_to_add = data['rowsToAdd']
        rows_to_delete = data['rowsToDelete']
        for row in rows_to_edit:
            new_values = {}
            print(row);
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
                return {"message": "Error occurred while deleting"}
            print(query);
            db[table_name].delete_one(query)

        if db['Metadata'].find_one({"Name": table_name})["containsWorkers"]:
            workers = True
        elif db['Metadata'].find_one({"Name": table_name})["containsGeo"]:
            workers = False
        else:
            return {"message": "Error occurred while adding"}
        for row in rows_to_add:
            new_value = {}
            if not workers:
                new_value['ID'] = get_sequence('loc')
            for key in row.keys():
                if key in allowed_keys:
                    new_value[key] = row[key]
            if workers is False and db[table_name].find_one({"Name": row["Name"]}) is None:
                db[table_name].insert_one(new_value)
            elif workers and db[table_name].find_one({"Telegram": row["Telegram"]}) is None:
                db[table_name].insert_one(new_value)
        return {"message": "Successfully done"}

    # to create a new table
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Name", type=str, required=True, help='Name cannot be left blank')
        parser.add_argument("keys", type=str, required=True, help='Params cannot be left blank')
        data = parser.parse_args()
        keys = eval(data["keys"])
        for key in db["Metadata"].find_one({"Name": "Required fields"})["keys"]:
            if key not in keys:
                return {"message": "Not all required keys specified"}
        if data["Name"] in db.list_collection_names():
            return {"message": "Table with this name already exists"}
        collection = db[data["Name"]]
        collection.insert_one({"Initial": "Initial"})
        db["Metadata"].insert_one({data['Name']: {
            "keys": keys,
            "containsWorkers": True,
            "containsGeo": False
        }})
        return {"message": "Collection successfully created"}

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Name", type=str, required=True, help='Name cannot be left blank')
        data = parser.parse_args()
        table_name = data['Name']
        try:
            db[table_name].drop()
            return {"message": "Successfully deleted"}
        except:
            return {"message": "An error occurred during deletion"}


def get_sequence(name):
    collection = db.sequences
    document = collection.find_one_and_update({"_id": name}, {"$inc": {"value": 1}}, return_document=True)
    return document["value"]
