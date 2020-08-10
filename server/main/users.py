"""Application routes."""
from datetime import datetime as dt
from flask import Blueprint, request, render_template, make_response, redirect, url_for,Response
from flask import current_app as app
from .models import db, User
from flask_restful import Resource, Api

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

@users_blueprint.route('/', methods=['GET'])
def user_records():
    """Create a user via query string parameters."""
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(f'{username} ({email}) already created!')
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days",
            admin=False
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for('user_records'))
    return render_template(
        'users.jinja2',
        users=User.query.all(),
        title="Show Users"
    )

@users_blueprint.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()

    email = body["email"]
    username = body["username"]
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(f'{username} ({email}) already created!')
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="I am the hero that gotham needs \
            I like long walks on the beach and reading time magazine",
            admin=False
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        
    return "hello"



class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}


class UsersPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


class Users(Resource):
    def get(self, user_id):
        """Get single user details"""
        response_object = {
            'status': 'fail',
            'message': 'User does not exist'
        }
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response_object, 404
            else:
                response_object = {
                    'status': 'success',
                    'data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'active': user.active
                    }
                }
                return response_object, 200
        except ValueError:
            return response_object, 404


# class UsersList(Resource):

#     method_decorators = {'post': [authenticate_restful]}

#     def get(self):
#         """Get all users"""
#         response_object = {
#             'status': 'success',
#             'data': {
#                 'users': [user.to_json() for user in User.query.all()]
#             }
#         }
#         return response_object, 200

#     def post(self, resp):
#         post_data = request.get_json()
#         response_object = {
#             'status': 'fail',
#             'message': 'Invalid payload.'
#         }
#         if not is_admin(resp):
#             response_object['message'] = \
#                 'You do not have permission to do that.'
#             return response_object, 401
#         if not post_data:
#             return response_object, 400
#         username = post_data.get('username')
#         email = post_data.get('email')
#         password = post_data.get('password')
#         try:
#             user = User.query.filter_by(email=email).first()
#             if not user:
#                 db.session.add(User(
#                     username=username, email=email, password=password)
#                 )
#                 db.session.commit()
#                 response_object['status'] = 'success'
#                 response_object['message'] = f'{email} was added!'
#                 return response_object, 201
#             else:
#                 response_object['message'] = \
#                     'Sorry. That email already exists.'
#                 return response_object, 400
#         except exc.IntegrityError:
#             db.session.rollback()
#             return response_object, 400
#         except (exc.IntegrityError, ValueError):
#             db.session.rollback()
#             return response_object, 400

api.add_resource(HelloWorld, '/users')
# api.add_resource(UsersPing, '/users/ping')
# api.add_resource(Users, '/users/<user_id>')
# api.add_resource(UsersList, '/users')