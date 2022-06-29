import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['GET', 'POST'])
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except exc.SQLAlchemyError:
        abort(500)
    except Exception:
        abort(422)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET', 'POST'])
def add_drink():
    data = request.get_json()
    title = data.get('title', None)
    color = data.get('color', None)
    name = data.get('name', None)
    parts = data.get('parts', None)
    details = [title, name, color, parts]

    if None in details or ' ' in details:
        abort(400, description="incomplete drink details")
        
    new_drink_recipe = [{'color': color, 'name':name, 'parts':parts}]

    try:
        new_drink = Drink(title=title, recipe = json.dumps(new_drink_recipe))
        new_drink.insert()
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except exc.SQLAlchemyError:
        abort(500)
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
def drinks_detail():
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except exc.SQLAlchemyError:
        abort(500)
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def update_drink(drink_id):
    drink = Drink.query.get(drink_id)

    if not drink:
        abort(404, description = "drink doesn't exist")

    data = request.get_json()
    title = data.get('title', None)
    color = data.get('color', None)
    name = data.get('name', None)
    parts = data.get('parts', None)

    try:
        drink_recipe = [{'color': color, 'name':name, 'parts':parts}]
        drink.title = title
        drink.recipe = drink_recipe
        drink.update()

        drinks = [drink.long() for drink in Drink.query.all()]
        
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except exc.SQLAlchemyError:
        abort(500)
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    drink = Drink.query.get(drink_id)

    if not drink:
        abort(404, description="drink doesn't exist")

    try:
        drink.delete()

        drinks = [drink.long() for drink in Drink.query.all()]
        
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except exc.SQLAlchemyError:
        abort(500)
    except Exception:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable entity"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
            jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "server error"
    }), 500


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def unauthorized(error):
    formatted_error = error.formatted()
    status_code = error.get('status_code', 401)
    return jsonify(formatted_error), status_code

