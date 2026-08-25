from db import db
from models.associations import store_categories


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    stores = db.relationship(
        "StoreModel",
        secondary=store_categories,
        back_populates="categories"
    )