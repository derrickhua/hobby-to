from marshmallow import Schema, fields

class HobbySchema(Schema):
    hobby_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    category = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

class LocationSchema(Schema):
    location_id = fields.Int(dump_only=True)
    hobby_id = fields.Int(required=True)
    name = fields.Str(required=True)
    address = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    cost = fields.Str()
    popularity = fields.Int()
    website = fields.Str()