from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Favorite, Character, Planet, Vehicle
# from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
# Que tipo de peticiones y de donde
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

# prueba users

@api.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    
    serialize_users = list([user.serialize() for user in users])
    print(serialize_users)
    return jsonify(serialize_users), 200

@api.route('/users/<int:userId>/fav', methods=['GET'])
def getFav(userId):
    user = User.query.get(userId)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    favorites = Favorite.query.filter_by(userId=userId).all()
    
    favorites_dict = {
        "favorite_characters": [],
        "favorite_planets": [],
        "favorite_vehicles": []
    }

    for favorite in favorites:
        if favorite.favoriteType == "character":
            character = Character.query.get(favorite.favoriteId)
            if character:
                favorites_dict["favorite_characters"].append(character.serialize())
        elif favorite.favoriteType == "planet":
            planet = Planet.query.get(favorite.favoriteId)
            if planet:
                favorites_dict["favorite_planets"].append(planet.serialize())
        elif favorite.favoriteType == "vehicles":
            vehicle = Vehicle.query.get(favorite.favoriteId)
            if vehicle:
                favorites_dict["favorite_vehicles"].append(vehicle.serialize())

    return jsonify(favorites_dict), 200


# adding favorites
@api.route('/favorite/user/<int:userId>', methods=['POST'])
def favoritePost(userId):
    user = User.query.get(userId)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    body = request.get_json()

    favoriteType = body.get('favoriteType')
    favoriteId = body.get('favoriteId')

    if not favoriteType or not favoriteId:
        return jsonify({"msg": "Missing favorite type or favorite ID"}), 400

    if favoriteType == 'character':
        favorite_item = Character.query.get(favoriteId)
    elif favoriteType == 'vehicles':
        favorite_item = Vehicle.query.get(favoriteId)
    elif favoriteType == 'planet':
        favorite_item = Planet.query.get(favoriteId)
    else:
        return jsonify({"msg": "Invalid favorite type"}), 400

    if not favorite_item:
        return jsonify({"msg": "Favorite item not found"}), 404

    newFavorite = Favorite(userId=user.id, favoriteType=favoriteType, favoriteId=favoriteId)
    db.session.add(newFavorite)
    db.session.commit()

    return jsonify({"msg": "Favorite added successfully"}), 200

# delete fav

@api.route('/favorites/users/<int:userId>/<string:type>/<int:id>', methods=['DELETE'])
def delete_favorite(userId, type, id):
    user = User.query.get(userId)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    favorite = Favorite.query.filter_by(userId=userId, favoriteType=type, favoriteId=id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite deleted successfully"}), 200


# people
@api.route('/characters', methods=['GET'])
def getCharacter():
    characters=Character.query.all()
    serialized_characters = list([character.serialize() for character in characters])
    
    return jsonify(serialized_characters), 200

@api.route('/characters/<int:characterId>', methods=['GET'])
def getCharacter_Id():
    character = Character.query.get(characterId)
    return jsonify(character.serialize()), 200

@api.route('/characters', methods=['POST'])
def newCharacter():
    body = request.get_json()

    if not body:
        return jsonify({"msg": "Missing JSON body"}), 400

    character = Character(
        name=body.get('name'),
        gender=body.get('gender'),
        eyeColor=body.get('eyeColor'),
        description=body.get('description'),
        imageUrl=body.get('imageUrl'),
        planetId=body.get('planetId')
    )

    if not character.name or not character.gender or not character.eyeColor or not character.planetId:
        return jsonify({"msg": "Missing required fields"}), 400

    db.session.add(character)
    db.session.commit()

    return jsonify(character.serialize()), 201
