from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

user_favorites = db.Table(
    'user_favorites',
    db.Column('user_id', ForeignKey='user.id'),
    db.Column('planet_id', ForeignKey='planet.id'),
    db.Column('character_id', ForeignKey='character.id')
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40))
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)

    favorites = db.relationship('Favorites', secondary=user_favorites, back_populates='user')

    def serialize_user(self):
        return {
        'name': self.name,
        'last_name': self.last_name,
        'email': self.email
        }


class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.Text)
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))

    favorites = db.relationship('Favorites', secondary=user_favorites, back_populates='user')


    def serialize_character(self):
        print(self.name)
        return({
            "name": self.name,
            'birth_year': self.birth_year,
            'gender': self.gender,
            'height': self.height,
            'skin_color': self.skin_color,
            'eye_color': self.eye_color
        })
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    climate = db.Column(db.String(20))
    population = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)

    favorites = db.relationship('Favorites', secondary=user_favorites, back_populates='user')

    def serialize_planet(self):
        return ({
            "name": self.name,
            'climate': self.climate,
            'population': self.population,
            'orbital_period': self.orbital_period,
            'rotation_period': self.rotation_period,
            'diameter': self.diameter
        })
    
class Nature(Enum):
    CHARACTER = 'character'
    PLANET = 'planet'

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    nature = db.Column(db.Enum(Nature), nullable=False)
    nature_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='favorites')
    character = db.relationship('Character', back_populates='favorites')
    # planet = db.relationship('Planet', back_populates='favorites')

    def serialize_favorite(self):
        return ({
        'character_id': self.character_id,
        'planet_id': self.planet_id
        })