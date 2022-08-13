"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

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
def get_members():
    family = jackson_family.get_all_members()
    return jsonify(family), 200

#BY ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member),200
    else:
        return jsonify({
            "fail": "id doesn't exist"
        }), 400

@app.route('/member', methods=['POST'])
def add_member():
    id = request.json.get('id')
    first_name = request.json.get('first_name')
    last_name = "Jackson"
    age = request.json.get('age')
    lucky_numbers = request.json.get('lucky_numbers')

    if not first_name:
        return jsonify({
            "message": "firstname required"
        }), 400
    if not last_name:
        return jsonify({
            "message": "Lastname required"
        }), 400
    if not age:
        return jsonify({
            "message": "Age required"
        }), 400
    if not lucky_numbers:
        return jsonify({
            "message": "Lucky number(s) is/are required"
        }), 400
        
    member = {
        'first_name': first_name,
        'age': age,
        'lucky_numbers': lucky_numbers,
        'id': id
    }

    jackson_family.add_member(member)
    return jsonify({
        "success": "Family Member created"
        }), 200

@app.route('/member/<int:id>', methods=['PUT'])     
def update_member(id):   

    member = jackson_family.get_member(id)
    first_name = request.json.get('first_name')
    last_name = "Jackson"
    age = request.json.get('age')
    lucky_numbers = request.json.get('lucky_numbers')

    if not first_name:
        return jsonify({
            "message": "firstname required"
        }), 400
    if not last_name:
        return jsonify({
            "message": "Lastname required"
        }), 400
    if not age:
        return jsonify({
            "message": "Age required"
        }), 400
    if not lucky_numbers:
        return jsonify({
            "message": "Lucky number(s) is/are required"
         }), 400
    if not id:
        return jsonify({
            "message": "no member has been found"
        }), 400

    member['first_name'] = first_name
    member['last_name'] = last_name
    member['age'] = age 
    member['lucky_numbers'] = lucky_numbers

    return jsonify({
        "message": "Family member updated "
    }), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.delete_member(member_id)
    if not member:
        return jsonify({
            "error": "Member doesn't exist"
        }), 400
    return jsonify(member)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
