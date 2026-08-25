from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.store import StoreModel
from models.category import CategoryModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
        @blp.response(200, StoreSchema)
        def get(self, store_id):
         store = StoreModel.query.get_or_404(store_id)
         return store
        
    
        def delete(self, store_id):
          store = StoreModel.query.get_or_404(store_id)
          db.session.delete(store)
          db.session.commit()
          return{"message":"Store Deleted"}    



        @blp.arguments(StoreSchema)
        @blp.response(200, StoreSchema)
        def put(self, store_data, store_id):
          store = StoreModel.query.get(store_id)

          if store:
            store.name = store_data["name"]
          else:
            store = StoreModel(**store_data)

          if "category_id" in store_data:
             category = CategoryModel.query.get_or_404(store_data["category_id"])
             store.categories.append(category)

          try:
           db.session.add(store)
           db.session.commit()
           return store
          except Exception:
            db.session.rollback()
            abort(500, message="An error occurred while updating/creating the store.")
                  
             
           
           
          
@blp.route("/store")
class StoreList(MethodView):

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):

        if StoreModel.query.filter(
            StoreModel.name == store_data["name"]
        ).first():
            abort(
                409,
                message="A store with that name already exists."
            )

        # category_id আলাদা করে নিচ্ছি
        category_id = store_data.pop("category_id", None)

        # # DEBUG: eta temporarily rakho
        # print("STORE DATA:", store_data)
        # print("CATEGORY ID:", category_id)

        # ekhane category_id thakar kotha NA
        store = StoreModel(**store_data)

        # category thakle many-to-many relationship create korchi
        if category_id is not None:
            category = CategoryModel.query.get_or_404(category_id)
            store.categories.append(category)

        try:
            db.session.add(store)
            db.session.commit()

        except Exception:
            db.session.rollback()
            abort(
                500,
                message="An error occurred while creating the store."
            )

        return store



