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
from models import db, User, People, Planet, Favorites
#from models import People

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
    people = People.query.all()

    return jsonify(list(map(lambda item: item.serialize(), people))), 200    

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    try:
        people = People.query.get(people_id)
        if people is None:
            return jsonify(f'The user with id {people_id} does not exist'), 404
        else:
            return jsonify(people.serialize()), 200
    except Exception as error:
        print(error)
        return jsonify('error'), 500
    
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()

    return jsonify(list(map(lambda item: item.serialize(), planets))), 200

@app.route('/planets/<int:planet_id>')
def get_one_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)

        if planet is None:
            return jsonify(f'Planet with id {planet_id} does not exist'), 404
        else:
            return jsonify(planet.serialize()), 200
    except Exception as error:
        print(error)
        return jsonify("error"), 500
    
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    return jsonify(list(map(lambda item: item.serialize(), users)))

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    try:
        favorites = Favorites.query.all()
        return jsonify(list(map(lambda item: item.serialize(), favorites)))
    except Exception as error:
        print(error)
        return jsonify('error')
  
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id=None):
    try:
        favorite = Favorites()
        favorite.planet_id = planet_id
        favorite.user_id = 1

        planet = Planet.query.get(planet_id)
        if planet is not None:
            db.session.add(favorite)
            db.session.commit()
            return jsonify('Added'), 200
        else:
            return jsonify(f'id {planet_id} does not exist'), 404
    except Exception as error:
        print(error)
        return jsonify('error'), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(people_id=None):
    try:
        favorite = Favorites()
        favorite.people_id = people_id
        favorite.user_id = 1

        people = Planet.query.get(people_id)
        if people is not None:
            db.session.add(favorite)
            db.session.commit()
            return jsonify('Added'), 200
        else:
            return jsonify(f'id {people_id} does not exist'), 404
    except Exception as error:
        print(error)
        return jsonify('error'), 500
    
@app.route('/favorite/planet/<int:id_planet>', methods=['DELETE'])
def delete_planet_favorite(id_planet=None):
    try: 
        planet_favorite = Favorites.query.filter_by(planet_id = id_planet).first()
        
        if planet_favorite is not None:
            db.session.delete(planet_favorite)
            db.session.commit()
            return jsonify('Deleted'), 200
        else:
            return jsonify(f'id {id_planet} does not exist'), 404
    except Exception as error:
        print(error.args)
        return jsonify('error'), 500
    
@app.route('/favorite/people/<int:id_people>', methods=['DELETE'])
def delete_people_favorite(id_people=None):
  
    people_favorite = Favorites.query.filter_by(people_id = id_people).first()
    
    if people_favorite is not None:
        db.session.delete(people_favorite)
        db.session.commit()
        return jsonify('Deleted'), 200
    else:
        return jsonify(f'id {id_people} does not exist'), 404
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
