"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_all_people():
    character = Character()
    character = character.query.all()

    return jsonify(list(map(lambda item: item.serialize_character(), character))), 200    

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    try:
        character = Character.query.get(people_id)
        if character is None:
            return jsonify(f'The user with id {people_id} does not exist'), 404
        else:
            return jsonify(character.serialize_character()), 200
    except Exception as error:
        print(error)
        return jsonify('error'), 500
    
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()

    return jsonify(list(map(lambda item: item.serialize_planet(), planets))), 200

@app.route('/planets/<int:planet_id>')
def get_one_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)

        if planet is None:
            return jsonify(f'Planet with id {planet_id} does not exist'), 404
        else:
            return jsonify(planet.serialize_planet()), 200
    except Exception as error:
        print(error)
        return jsonify("error"), 500
    
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    return jsonify(list(map(lambda item: item.serialize_user(), users)))

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    favorites = Favorites.query.all()
    return jsonify(list(map(lambda item: find_id(item.serialize_favorite()), favorites)))

def find_id(favorite):
    character = Character.query.get(favorite['character_id'])
    planet = Planet.query.get(favorite['planet_id'])

    if planet is not None: 
        return planet.serialize_planet()
    if character is not None:
        return character.serialize_character()
  
    
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
