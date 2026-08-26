from marshmallow import Schema, fields, validate


class StoreShortSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    
class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate= validate.Length(min=2, max=50), error_messages={"required": "Item name is required."})
    price = fields.Float(required=True, validate=validate.Range(min=0.01), error_messages={"required": "Price is required."})
    store_id = fields.Int(required=True, error_messages={"required": "Store ID is required."})
    store = fields.Nested(StoreShortSchema, dump_only=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)



class StoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    items = fields.Nested("ItemSchema", dump_only=True, many=True)
    categories = fields.Nested(CategorySchema, dump_only=True, many=True)
    category_id = fields.Int( required=False)
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)