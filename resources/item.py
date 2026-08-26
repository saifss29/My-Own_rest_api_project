from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.item import ItemModel
from schemas import ItemSchema
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp = Blueprint("items", __name__,  description= "Operation on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return{"message": "Item deleted"}

    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
         item.name = item_data["name"]
         item.price = item_data["price"]
        else:
           item = ItemModel( **item_data)

        db.session.add(item)
        db.session.commit()
        return(item) 


@blp.route("/item")
class ItemList(MethodView):
   @jwt_required(fresh=True)
   @blp.arguments(ItemSchema)
   @blp.response(201, ItemSchema)
   def post(self, item_data):
      item = ItemModel(**item_data)

      try:
       db.session.add(item)
       db.session.commit()
      except IntegrityError:
        abort(400, message="An item with that name already exists.")
      except SQLAlchemyError:
        abort(500, message="An error occurred while inserting the item.")
      return item
        