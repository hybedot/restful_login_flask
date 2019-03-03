from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import RegisterUser, LoginUser
from resources.admin import Users, PromoteUser, UserList
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'ibrahim'
api = Api(app)

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(RegisterUser, '/register')
api.add_resource(LoginUser, '/login')
api.add_resource(Users, '/admin/<string:username>')
api.add_resource(UserList, '/admin/users')
api.add_resource(PromoteUser, '/admin/promoteuser/<string:username>')

if __name__ == "__main__":
    from db import db 
    db.init_app(app)
    app.run(debug = True)