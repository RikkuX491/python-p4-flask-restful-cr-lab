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
        response_body = [plant.to_dict() for plant in Plant.query.all()]

        return make_response(response_body, 200)
    
    def post(self):
        new_plant = Plant(name=request.json.get('name'), image=request.json.get('image'), price=request.json.get('price'))
        db.session.add(new_plant)
        db.session.commit()

        response_body = new_plant.to_dict()

        return make_response(response_body, 201)
    
api.add_resource(Plants, "/plants")

class PlantByID(Resource):
    
    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()

        if plant:
            response_body = plant.to_dict()
            return make_response(response_body, 200)
        else:
            response_body = {
                'error': 'Plant Not Found'
            }
            return make_response(response_body, 404)

api.add_resource(PlantByID, "/plants/<int:id>")      

if __name__ == '__main__':
    app.run(port=5555, debug=True)
