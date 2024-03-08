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

class RoadmapSchema(Schema):
    roadmap_id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    hobby_id = fields.Int(required=True)
    user_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class RoadmapNodeSchema(Schema):
    node_id = fields.Int(dump_only=True)
    roadmap_id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    order = fields.Int(required=True)
    parent_node_id = fields.Int(allow_none=True)
    estimated_time = fields.Str()