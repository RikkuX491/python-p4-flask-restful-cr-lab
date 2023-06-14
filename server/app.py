#!/usr/bin/env python3

import ipdb
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    
    def get(self):
        plants = Plant.query.all()
        response_body = []
        for plant in plants:
            plant_dictionary = {
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': plant.price
            }
            response_body.append(plant_dictionary)

        return make_response(jsonify(response_body), 200)
    
    def post(self):
        new_plant = Plant(name=request.get_json().get('name'), image=request.get_json().get('image'), price=request.get_json().get('price'))
        db.session.add(new_plant)
        db.session.commit()

        response_body = {
            "id": new_plant.id,
            "name": new_plant.name,
            "image": new_plant.image,
            "price": new_plant.price
        }

        return make_response(jsonify(response_body), 201)
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    
    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()

        if not plant:
            response_body = {
                "error": "Plant not found"
            }
            status = 404

        else:
            response_body = {
                "id": plant.id,
                "name": plant.name,
                "image": plant.image,
                "price": plant.price
            }
            status = 200

        return make_response(jsonify(response_body), status)

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
