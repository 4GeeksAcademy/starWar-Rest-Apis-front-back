from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Favorites, Character, Planet, Vehicle
from api.utils import generate_sitemap, APIException
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

@api.route('/users/<int:userId/fav', methods=['GET'])
def getFav():
    user = User.query.all(userId)
    favorites = Favorites.query.filter_by(userId=userId).all()
    print(favorites)

    favorites_dict = {
            "favorite_characters": [],
            "favorite_planets": [],
            "favorite_vehicles": []
        }
    for favorite in favorites:
        if favorite.favoriteType == "character":
            character = Character.query.get(favorite.favoriteId)
            print(character)
        if character:
            favorites_dict["favorite_characters"].append(character.name)
        elif favorite.favoriteType == "planet":
            planet = Planet.query.get(favorite.favoriteId)
        if planet:
            favorites_dict["favorite_planets"].append(planet.name)
        elif favorite.favoriteType == "vehicles":
            vehicle = Vehicle.query.get(favorite.favoriteId)
        if vehicle:
            favorites_dict["favorite_vehicles"].append(vehicle.name)
        return jsonify(favorites_dict), 200

# adding favorites
@api.route('/favorite/user/<int:userId>', methods=['POST'])
def favoritePost():
    user=User.query.get(userId)

    body = request.get_json()

    favoriteType = body.get('favoriteType')
    favoriteId = body.get('favoriteId')

    if favoriteType == 'character':
        favorite_item = Character.query.get(favoriteId)
    elif favoriteType == 'vehicles':
        favorite_item = Vehicle.query.get(favoriteId)
    elif favoriteType == 'planet':
        favorite_item = Planet.query.get(favoriteId)

    newFavorite = Favorites(user_id=user.id, favorite_type=favoriteType, favorite_id=favoriteId)
    db.session.add(newFavorite)
    db.session.commit()

    return jsonify({"msg": "successfully"}), 200
    
# delete

