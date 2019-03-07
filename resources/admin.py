from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, fresh_jwt_required
from werkzeug.security import  generate_password_hash

from models.user import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )



class Users(Resource):
    @jwt_required
    def get(self, username):
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        if not current_user.admin:
            return {'message':'unauthorised user'}, 401
        
        user = UserModel.find_by_username(username)
        if user:            
            return {'user_id': user.id,
                    'username': user.username
                    }
        
        return {'message': 'user not found'}, 404
    
    @fresh_jwt_required
    def delete(self, username):
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)

        if not current_user.admin:
            return {'message':'unauthorised user'}, 401
            
        user = UserModel.find_by_username(username)
        if user:                
            user.delete_from_db()
            return {'message':'user deleted'}
        
        return {'message':'unable to delete user'}, 500
    
class PromoteUser(Resource):
    @fresh_jwt_required
    def put(self):
        _user_parser.add_argument('id',
                                   type=str,
                                   required=True,
                                   help="This field cannot be blank."
                                )

        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)

        if not current_user.admin:
            return {'message':'unauthorised user'}, 401

        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            user.admin = True
            user.save_to_db()
            return {'message':'the user has been promoted to an admin'}

class UserList(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        
        if not current_user.admin:
            return {'message':'unauthorised user'}, 401

        return {'users': [x.json() for x in UserModel.find_all()]}

        