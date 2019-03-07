from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt)

from models.user import UserModel
from blacklist import BLACKLIST

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
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access token': access_token,
                'refresh token': refresh_token
            }, 200
        
        return{'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200




    
    
