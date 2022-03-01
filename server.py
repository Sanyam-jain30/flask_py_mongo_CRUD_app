from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient("<Mongo atlas connection link>")
    db = mongo.get_database('customer')
    mongo.server_info()

except:
    print("ERROR - Cannot connect to db")

# Read

@app.route("/customers", methods=["GET"])
def get_some():
    try:
        dbResponse = list(db.customer.find())
        for ele in dbResponse:
            ele["_id"] = str(ele["_id"])

        return Response(
            response = json.dumps(dbResponse),
            status = 200,
            mimetype = "application/json"
        )

    except Exception as e:
        print(e)
        return Response(
            response = json.dumps({"message": "cannot get customers"}),
            status = 500,
            mimetype = "application/json"
        )

# Create

@app.route("/customers", methods=["POST"])
def create_new():
    try:
        customer = {"name": request.form["name"], "product": request.form["product"]}
        dbResponse = db.customer.insert_one(customer)

        print(dbResponse.inserted_id)
        # for ele in dir(dbResponse):
        #     print(ele)

        return Response(
            response = json.dumps({
                "message": "customer added", 
                "id": f"{dbResponse.inserted_id}"
                }),
            status = 200,
            mimetype = "application/json"
        )

    except Exception as e:
        print(e)

# Update

@app.route("/customers/<id>", methods=["PATCH"])
def update_customer(id):
    try:
        dbResponse = db.customer.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"]}}
        )

        if dbResponse.modified_count == 1:
            return Response(
                response = json.dumps({"message": "customer updated"}),
                status = 200,
                mimetype = "application/json"
            )

        return Response(
            response = json.dumps({"message": "nothing to update"}),
            status = 200,
            mimetype = "application/json"
        )

    except Exception as e:
        print(e)
        return Response(
            response = json.dumps({"message": "Sorry! cannot update"}),
            status = 500,
            mimetype = "application/json"
        )


# Delete

@app.route("/customers/<id>", methods=["DELETE"])
def delete_customer(id):
    try:
        dbResponse = db.customer.delete_one({"_id": ObjectId(id)})

        if dbResponse.deleted_count == 1: 
            return Response(
                response = json.dumps({
                    "message": "customer deleted",
                    "id": f"{id}"
                }),
                status = 200,
                mimetype = "application/json"
            )

        return Response(
            response = json.dumps({
                "message": "customer not found!",
                "id": f"{id}"
            }),
            status = 200,
            mimetype = "application/json"
        )

    except Exception as e:
        print(e)
        return Response(
            response = json.dumps({"message": "Sorry! cannot delete customer"}),
            status = 500,
            mimetype = "application/json"
        )

if __name__ == "__main__":
    app.run(port = 5000, debug = True)
