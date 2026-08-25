from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import CategorySchema
from models.category import CategoryModel



blp= Blueprint("categories", __name__, description= "Operation on items")

@blp.route("/category/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return{"message": "category deleted"}
    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def put(self, category_data, category_id):
        category = CategoryModel.query.get(category_id)

        if category:
            category.name = category_data["name"]
            
        else:
            category = CategoryModel(**category_data)

        db.session.add(category)
        db.session.commit()
        return category


@blp.route("/category")
class CategoryList(MethodView):
    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)

        db.session.add(category)
        db.session.commit()
        return category

    

