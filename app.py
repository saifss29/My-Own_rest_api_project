import os
from db import db
from dotenv import load_dotenv
from flask_smorest import Api
from flask import Flask
from models.store import StoreModel
from models.item import ItemModel
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from config import DevelopmentConfig,ProductionConfig


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

api = Api(app)

api.register_blueprint(StoreBlueprint)
api.register_blueprint(ItemBlueprint)
print(app.url_map)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
