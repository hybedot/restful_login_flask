from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from werkzeug.security import  generate_password_hash

from models.user import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

class Users(Resource):
    
    @jwt_required()
    def get(self, username):
        current_user = current_identity
        if not current_user.admin:
            return {'message':'unauthorised user'}, 401
        
        user = UserModel.find_by_username(username)
        if user:            
            return {'user_id': user.id,
                    'username': user.username
                    }
        
        return {'message': 'user not found'}, 404

    @jwt_required()
    def post(self, username):
        current_user = current_identity
        if not current_user.admin:
            return {'message':'unauthorised user'}, 401

        data = _user_parser.parse_args()
        user =  UserModel.find_by_username(data['username'])
        if user:
            return {'message':'user already exits'}
        
        hashed_password = generate_password_hash(data['password'], method='sha256')
        user = UserModel(data['username'], hashed_password)
        
        try:
            user.save_to_db()
        except:
            return {'message':'unable to create user'}, 500

        #return {'message':'user successfuly created'}, 201
        return {'username': data['username'],
                'password': hashed_password}, 201
    
    @jwt_required()
    def delete(self, username):
        current_user = current_identity
        if not current_user.admin:
            return {'message':'unauthorised user'}, 401
            
        user = UserModel.find_by_username(username)
        if user:                
            user.delete_from_db()
            return {'message':'user deleted'}
        
        return {'message':'unable to delete user'}, 500
    
class PromoteUser(Resource):
    @jwt_required()
    def put(self, username):
        current_user = current_identity
        if not current_user.admin:
            return {'message':'unauthorised user'}, 401

        user = UserModel.find_by_username(username)
        if user:
            user.admin = True
            user.save_to_db()
            return {'message':'you have been promoted to an admin'}

class UserList(Resource):
    @jwt_required()
    def get(self):
        current_user = current_identity
        if not current_user.admin:
            return {'message':'unauthorised user'}, 401

        return {'users': [x.json() for x in UserModel.find_all()]}

        



