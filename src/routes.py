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

    # Buscar el personaje por ID
@api.route('/characters/<int:character_id>', methods=['PUT'])
def editCharacter(character_id):
    character = Character.query.filter_by(id=character_id).first()

    
    if not character:
        return jsonify({"msg": "Character not found"}), 404

    
    body = request.get_json()

    if not body:
        return jsonify({"msg": "Missing JSON body"}), 400

    
    character.name = body.get('name', character.name)
    character.gender = body.get('gender', character.gender)
    character.eyeColor = body.get('eyeColor', character.eyeColor)
    character.description = body.get('description', character.description)
    character.imageUrl = body.get('imageUrl', character.imageUrl)
    character.planetId = body.get('planetId', character.planetId)

    
    db.session.commit()

    
    return jsonify({"msg": "Character has been edited successfully", "character": character.serialize()}), 200

    # Delete Character

@api.route('/characters/<int:character_id>', methods=['DELETE'])
def deleteCharacter(characterId):
    character=Character.query.filter_by(id = characterId).first()
    if not character:
        return jsonify({"msg": "Character not found"}), 404
    serialized_character = character.serialize()
    db.session.delete(character)
    db.session.commit()

    return jsonify('Character has been deleted successfully', serialized_character), 200

    # Planets

@api.route('/planets', methods=['GET'])
def getPlanets():
    planets=Planet.query.all()
    serialized_planets = list([planet.serialize() for planet in planets])
    if not planets:
        return jsonify("No planets found", status_code=404)
    else:
        return jsonify(serialized_planets), 200
    
@api.route('/planets/<int:planet_id>', methods=['GET'])
def getPlanet(planetId):
    planet = Planet.query.get(planetId)
    if not planet:
        return jsonify("Character not found", status_code=404)
    else:
        return jsonify(planet.serialize()), 200
    
@api.route('/planets', methods=['POST'])
def planetPost():
    body = request.get_json()
    if not body:
        return jsonify("Request body is empty", status_code=400)
    
    planet=Planet()
    planet.name = body.get('name')
    planet.population=body.get('population')
    planet.climate=body.get('climate')
    planet.diameter=body.get('diameter')
    planet.description=body.get('description')
    planet.imageUrl=body.get('imageUrl')


    if not planet.name:
        return jsonify("Name is required", status_code=400)
    if not planet.population:
        return jsonify("Population is required", status_code=400)
    if not planet.climate:
        return jsonify("Climate is required", status_code=400)
    if not planet.diameter:
        return jsonify("Diameter is required", status_code=400)
   
  
    
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 201

@api.route('/planets/<int:planet_id>', methods=['PUT'])
def editPlanet(planetId):
    planet=Planet.query.filter_by(id = planetId).first()
    if not planet:
        return jsonify("Planet not found", status_code=404)
    
    body= request.get_json()
    if not body:
        return jsonify("Request body is empty", status_code=400)

    planet.name = body.get('name', planet.name)
    planet.population=body.get('population', planet.population)
    planet.climate=body.get('climate', planet.climate)
    planet.diameter=body.get('diameter', planet.diameter)
    

    db.session.commit()

    return jsonify('Planet has been edit successfully',planet.serialize()), 200

@api.route('/planets/<int:planet_id>', methods=['DELETE'])
def deletePlanet(planetId):
    planet=Planet.query.filter_by(id = planetId).first()
    print(planet)
    if not planet:
        return jsonify("Planet not found", status_code=404)

    db.session.delete(planet)
    db.session.commit()

    return jsonify('Planet has been deleted successfully',planet.serialize()), 200

    # Vehicles

@api.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def getVehicle(vehicleId):
    vehicle = Vehicle.query.get(vehicleId)
    if not vehicle:
        return jsonify("Vehicle not found", status_code=404)
    else:
        return jsonify(vehicle.serialize()), 200

@api.route('/vehicles', methods=['POST'])
def vehiclePost():
    body = request.get_json()
    if not body:
        return jsonify("Request body is empty", status_code=400)
    
    vehicle=Vehicle()
    vehicle.name = body.get('name')
    vehicle.model=body.get('model')
    vehicle.vehicleClass=body.get('vehicleClass')
    vehicle.length=body.get('length')
    vehicle.description=body.get('description')
    vehicle.imageUrl=body.get('imageUrl')
    vehicle.pilotId=body.get('pilotId')

    if not vehicle.name:
        return jsonify("Name is required", status_code=400)
    if not vehicle.model:
        return jsonify("Model is required", status_code=400)
    if not vehicle.vehicleClass:
        return jsonify("Vehicle class is required", status_code=400)
    if not vehicle.length:
        return jsonify("Length is required", status_code=400)
    if not vehicle.pilotId:
        return jsonify("Pilot ID is required", status_code=400)
    
    db.session.add(vehicle)
    db.session.commit()
    return jsonify(vehicle.serialize()), 201

@api.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def editVehicle(vehicle_id):
    vehicle=Vehicle.query.filter_by(id = vehicle_id).first()
    if not vehicle:
        return jsonify("Vehicle not found", status_code=404)
    
    body= request.get_json()
    if not body:
        return jsonify("Request body is empty", status_code=400)

    vehicle.name = body.get('name', vehicle.name)
    vehicle.model=body.get('model', vehicle.model)
    vehicle.vehicleClass=body.get('vehicleClass', vehicle.vehicleClass)
    vehicle.length=body.get('length', vehicle.length)
    vehicle.description=body.get('description', vehicle.description)
    vehicle.imageUrl=body.get('imageUrl', vehicle.imageUrl)
    vehicle.pilotId=body.get('pilotId', vehicle.pilotId)

    db.session.commit()
    
    return jsonify('Planet has been edit successfully',vehicle.serialize()), 200

@api.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def deleteVehicle(vehicle_id):
    vehicle=Vehicle.query.filter_by(id = vehicle_id).first()
    if not vehicle:
        return jsonify("Vehicle not found", status_code=404)
    serialized_vehicle= vehicle.serialize()
    db.session.delete(vehicle)
    db.session.commit()

    return jsonify('Vehicle has been deleted successfully', serialized_vehicle), 200  
   
    

    
