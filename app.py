import os
from db import db
from dotenv import load_dotenv
from flask_smorest import Api
from flask import Flask,jsonify
from models.store import StoreModel
from models.item import ItemModel
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.category import blp as CategoryBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST
from flask_migrate import Migrate

from config import DevelopmentConfig,ProductionConfig
from flask_jwt_extended import JWTManager



load_dotenv()

app = Flask(__name__)

env = os.getenv("FLASK_ENV", "development")

if env == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

print("Current ENV:", env)
print("DEBUG:", app.config["DEBUG"])
  


db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app,db)

api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return(
        jsonify({"message": "The token was revoked", "error":"Token revoked"})
       ,401
    )
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return(
        jsonify({"description": "Token is not fresh","error":"fresh token required"}),401
    )

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"message": "Signature verification failed.", "error": "invalid_token"}),
        401,
    )
@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify({"message": "Request does not contain an access token.", "error": "authorization_required"}),
        401,
    )

api.register_blueprint(StoreBlueprint)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(CategoryBlueprint)
api.register_blueprint(UserBlueprint)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

