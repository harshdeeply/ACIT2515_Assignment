import json

from flask import Flask, request

from bed import Bed
from furniture_manager import FurnitureManager
from sofa import Sofa

app = Flask(__name__)
my_store = FurnitureManager("furniture.sqlite")


@app.route("/furnituremanager/items", methods=["POST"])
def add_item():
    """ Creates and adds a new item to the furniture shop using the JSON info provided """
    data = request.json
    response_dict = {"status": 200, "response": None}

    try:
        item_type = data.pop("type", None)
        item_id = None

        if item_type == Bed.FURNITURE_TYPE:
            item_id = my_store.add(Bed(**data))
        elif item_type == Sofa.FURNITURE_TYPE:
            item_id = my_store.add(Sofa(**data))

        response_dict["response"] = "Id of new item added: " + str(item_id)

    except (ValueError, KeyError) as e:
        response_dict["status"] = 400
        response_dict["response"] = str(e)

    return app.response_class(**response_dict)


@app.route("/furnituremanager/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    """ Updates a furniture item using the given item_id, from the furniture store """
    item_id = int(item_id)
    data = request.json
    response_dict = {
        'status': 200
    }

    item = my_store.get(item_id)

    if item:
        #  Create a new item with all the updated properties
        #  and assign the same ID to it as the item being
        #  replaced.

        item_type = data.pop('type', None)
        updated_item = None

        if item_type == Bed.FURNITURE_TYPE:
            updated_item = Bed(**data)
        elif item_type == Sofa.FURNITURE_TYPE:
            data["number_of_seats"] = int(data["number_of_seats"])
            data["number_of_cushions"] = int(data["number_of_cushions"])
            updated_item = Sofa(**data)

        updated_item.id = item_id
        my_store.update(updated_item)

        response_dict["response"] = (
            "Item of ID " + str(item_id) + " successfully updated."
        )


    else:
        response_dict['status'] = 404
        response_dict["response"] = "No item was found corresponding to the given item_id"

    return app.response_class(**response_dict)


@app.route("/furnituremanager/items/<item_id>", methods=["DELETE"])
def remove_item(item_id):
    """ Removes an item using the given item_id, from the furniture store """
    item_id = int(item_id)
    response_dict = {"status": 200}

    item = my_store.get(item_id)

    if item:
        my_store.delete(item_id)
        response_dict["response"] = (
            "Item of ID " + str(item_id) + " successfully removed."
        )
    else:
        response_dict["status"] = 404
        response_dict[
            "response"
        ] = "No item was found corresponding to the given item_id"

    return app.response_class(**response_dict)


@app.route("/furnituremanager/items/<item_id>", methods=["GET"])
def get_item(item_id):
    """ Gets an item (JSON) using the given item_id, from the furniture store """
    item_id = int(item_id)
    response_dict = {"status": 200}

    item = my_store.get(item_id)

    if item:
        response_dict["response"] = json.dumps(item.to_dict())
    else:
        response_dict["status"] = 404
        response_dict[
            "response"
        ] = "No item was found corresponding to the given item_id"

    return app.response_class(**response_dict)


@app.route("/furnituremanager/items/all", methods=["GET"])
def get_all_items():
    """ Gets all items (JSON) from the furniture store """
    return app.response_class(
        status=200, response=json.dumps([item.to_dict() for item in my_store.get_all()])
    )


@app.route("/furnituremanager/items/all/<type>", methods=["GET"])
def get_all_items_type(type):
    """ Gets items of the specified type and sends them in the response (JSON) """
    response_dict = {"status": 200}

    if type == Bed.FURNITURE_TYPE or type == Sofa.FURNITURE_TYPE:
        response_dict["response"] = json.dumps(
            [item.to_dict() for item in my_store.get_all_by_type(type)]
        )
    else:
        response_dict["status"] = 400
        response_dict["response"] = "Given item type is not supported"

    return app.response_class(**response_dict)


@app.route("/furnituremanager/items/all/descriptions/<type>", methods=["GET"])
def get_all_descriptions(type):
    """ Gets all descriptions of items of the specified type and sends them in the response (JSON) """
    response_dict = {"status": 200}

    if type == Bed.FURNITURE_TYPE or type == Sofa.FURNITURE_TYPE:
        response_dict["response"] = json.dumps(
            [
                {"id": item.id, "desc": item.get_item_description()}
                for item in my_store.get_all_by_type(type)
            ]
        )
    else:
        response_dict["status"] = 400
        response_dict["response"] = "Given item type is not supported"

    return app.response_class(**response_dict)


@app.route("/furnituremanager/items/stats", methods=["GET"])
def get_furniture_stats():
    """ Gets statistics for the furniture store and sends them in the response (JSON) """
    return app.response_class(
        status=200,
        response=json.dumps(my_store.get_furniture_stats().to_dict()),
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(debug=True)
