from marshmallow import Schema, fields, validate


class StoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate= validate.Length(min=2, max=50), error_messages={"required": "Item name is required."})
    price = fields.Float(required=True, validate=validate.Range(min=0.01), error_messages={"required": "Price is required."})
    store_id = fields.Int(required=True, error_messages={"required": "Store ID is required."})