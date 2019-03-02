from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

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


class RegisterUser(Resource):    
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message':'user already exit'}, 400
        
        hashed_password = generate_password_hash(data['password'], method='sha256')
        user = UserModel(data['username'], hashed_password)

        try:
            user.save_to_db()
        except:
            return {'message':'unable to create user'}, 500

        #return {'message':'user succefully created'}, 201
        return {'username': data['username'],
                'password': hashed_password}, 201

class LoginUser(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user =  UserModel.find_by_username(data['username'])
    
        if user and  check_password_hash(user.password, data['password']):
            return {'message':'user logged in'}


    
    
