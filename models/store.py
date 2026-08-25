from db import db
from models.associations import store_categories





class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable = False)
    items = db.relationship("ItemModel", back_populates= "store")
    categories = db.relationship("CategoryModel", secondary= store_categories, back_populates="stores")
    





