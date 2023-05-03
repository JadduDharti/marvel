from flask import Blueprint, request, jsonify
from marvel.helpers import token_required, get_character_image
from marvel.models import db, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/characters', methods=['POST'])
@token_required
def create_character(our_user):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    image_url = get_character_image(request.json['name'])
    user_token = our_user.token

    character = Character(name, description, comics_appeared_in, super_power, image_url, user_token=user_token)
    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)

# READ all characters
@api.route('/characters', methods=['GET'])
@token_required
def get_characters(our_user):
    owner = our_user.token
    characters = Character.query.filter_by(user_token=owner).all()
    response = characters_schema.dump(characters)

    return jsonify(response)

# READ one character by ID
@api.route('/characters/<id>', methods=['GET'])
@token_required
def get_character(our_user, id):
    if id:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID required'}), 401

# UPDATE a character by ID
@api.route('/characters/<id>', methods=['PUT'])
@token_required
def update_character(our_user, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.image_url = get_character_image(request.json['name'])
    character.user_token = our_user.token

    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)

# DELETE a character by ID
@api.route('/characters/<id>', methods=['DELETE'])
@token_required
def delete_character(our_user, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)