from db import db

store_categories = db.Table(
    "store_categories",
    db.Column(
        "store_id",
        db.Integer,
        db.ForeignKey("stores.id"),
        primary_key=True
    ),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("categories.id"),
        primary_key=True
    )
)
  