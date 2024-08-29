from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite = db.relationship('Favorite', backref='user', lazy=True )


    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favoriteType=db.Column(db.Enum('character','vehicles','planet', name='favorite_type'), nullable=False)
    favoriteId=db.Column(db.Integer, nullable=False)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.Enum('female', 'male', 'other', 'n/a', name="genderTy"), nullable=False)
    eyeColor = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(500))
    imageUrl = db.Column(db.String(500))
    planetId = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    vehicle = db.relationship('Vehicle', backref='character', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.id
        
    def serialize(self):
        planetName = self.planet.name if self.planet else ''
        return{ 
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eyeColor": self.eyeColor,
            "description": self.description,
            "imageUrl": self.imageUrl,
            "homeworld": planetName,
        }
        
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    climate = db.Column(db.Enum('arid', 'tropical', 'frozen', name="climateTy"), nullable=False)   
    population = db.Column(db.Integer, unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(500))
    imageUrl = db.Column(db.String(500))
    character = db.relationship('Character', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id
            
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "diameter": self.diameter,
            "description": self.description,
            "imageUrl": self.imageUrl,
        }
        
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    model = db.Column(db.String(100), unique=False, nullable=False)
    vehicleClass = db.Column(db.String(100), unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(500))
    imageUrl = db.Column(db.String(500))
    pilotId = db.Column(db.Integer, db.ForeignKey('character.id'))
            
            
    def __repr__(self):
        return '<Vehicle %r>' % self.id
            
    def serialize(self):
        pilotName = self.character.name if self.character else ''
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicleClass": self.vehicleClass,
            "length": self.length,
            "description": self.description,
            "imageUrl": self.imageUrl,
            "pilotId": pilotName,
        }