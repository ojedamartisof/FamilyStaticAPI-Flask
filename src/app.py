"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def all_members():
    members = jackson_family.get_all_members()

    return jsonify(members), 200


@app.route('/member/<int:id>', methods=['GET'])
def one_member(id):
    members = jackson_family.get_member(id)
    if len(members) == 0:
        return jsonify({"msg": "Member not found"}), 404
    else:
        return jsonify(members), 200


@app.route('/member', methods=['POST'])
def create_member():
    id = request.json.get("id")
    first_name = request.json.get("first_name")
    last_name = "Jackson"
    age = request.json.get("age")
    lucky_numbers = request.json.get("lucky_numbers")

    if not id:
        id = jackson_family._generateId()
    if not first_name:
        return jsonify({"msg": "first_name is required"}), 400
    if not age:
        return jsonify({"msg": "age is required"}), 400
    if not lucky_numbers:
        return jsonify({"msg": "lucky_numbers is required"}), 400

    new_member = {}
    new_member['id'] = id
    new_member['first_name'] = first_name
    new_member['last_name'] = last_name
    new_member['age'] = age
    new_member['lucky_numbers'] = lucky_numbers

    jackson_family.add_member(new_member)
    return jsonify({"msg": "Member added succesfully"}), 200


@app.route('/members', methods=['PUT'])
def update_one_member():
    id = request.json.get("id")
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    age = request.json.get("age")
    lucky_numbers = request.json.get("lucky_numbers")

    if not id:
        return jsonify({"msg": "id is required"}), 400
    if not first_name:
        return jsonify({"msg": "first_name is required"}), 400
    if not last_name:
        return jsonify({"msg": "last_name is required"}), 400
    if not age:
        return jsonify({"msg": "age is required"}), 400
    if not lucky_numbers:
        return jsonify({"msg": "lucky_numbers is required"}), 400

    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"msg": "Member not found"}), 404
    if member:
        member['id'] = id
        member['first_name'] = first_name
        member['last_name'] = last_name
        member['age'] = age
        member['lucky_numbers'] = lucky_numbers

        jackson_family.update_member(id, member)

        return jsonify({"msg": "Member updated succesfully"}), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if not member:
        return jsonify({"msg": "Member not found"}), 404
    else:
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)