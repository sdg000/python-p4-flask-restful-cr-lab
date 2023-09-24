#!/usr/bin/env python3

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

# creating restful route for Home Class/Resources
class Home(Resource):

    def get(self):

        response_dict = {
            'message': 'starting backend server',
        }

        response = make_response(
            response_dict,
            200
        )
        return response
api.add_resource(Home, '/')


# creating restful route for Plant Resources  POST / GET 
class Plants(Resource):

    # method to return all Plant Instances
    def get(self):
        plants_dict = [plant.to_dict() for plant in Plant.query.all()]
        
        response = make_response(
            plants_dict,
            200
        )
        return response
    
    # method to create a Plant Instance
    def post(self):

        # save incoming post params
        data = request.get_json()

        # use incoming post params to create a new instance
        new_plant = Plant(
            name = data.get('name'),
            image = data.get('image'),
            price = data.get('price')

        )

        # save newly create instance to database
        db.session.add(new_plant)
        db.session.commit()

        # return newly created instance as dictionary
        respone = make_response(
            new_plant.to_dict(),
            201
        )
        return respone

    
# restful route ( GET, POST ) for Plants Class / Resource
api.add_resource(Plants, '/plants')


# creating restful route for Plant Instances   GET / PATCH / DELETE
class PlantByID(Resource):

    # find plant using id
    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        plant_dict = plant.to_dict()

        response = make_response(
            plant_dict,
            200
        )
        return response
    
    # update a plant instance 
    def patch(self, id):

        # find plant using id
        plant = Plant.query.filter(Plant.id == id).first()

        # save incoming post params
        data = request.get_json()

        # check content of incoming params 
        if 'name' in data:
            plant.name = data['name']

        if 'image' in data:
            plant.image = data['image']

        if 'price' in data:
            plant.price = data['price']

        # save updated instance to database
        db.session.add(plant)
        db.session.commit()

        # return updated instance as dictionary
        response = make_response(
            plant.to_dict(),
            200
        )
        return response

        
    # delete a plant instance 
    def delete(self, id):

        # find plant using id
        plant = Plant.query.filter(Plant.id == id).first()

        # delete from database 
        db.session.delete(plant)
        db.session.commit()

        # return response
        response_body = {
            'delete_successful': True,
            'message': 'Messaege Deleted'
        }

        response = make_response(
            response_body,
            200
        )

        return response

api.add_resource(PlantByID, '/plants/<int:id>')



# including a non-restful route among flask restful routes
@app.route('/plants/most-expensive')
def most_expensive():
    most_expensive = Plant.query.order_by(Plant.price.desc()).first()

    most_expensive_dict = most_expensive.to_dict()
    response = make_response(
        most_expensive_dict, 200
    )
    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
