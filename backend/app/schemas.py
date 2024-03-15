from marshmallow import Schema, fields
from marshmallow.validate import Length

class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=Length(min=1))
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)

class UserHobbySchema(Schema):
    user_hobby_id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    hobby_id = fields.Int(required=True)
    status = fields.Str()
    progress_notes = fields.Str()

class HobbySchema(Schema):
    hobby_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    sub_category = fields.Str(allow_none=True)  
    created_at = fields.DateTime(dump_only=True)

class LocationSchema(Schema):
    location_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    cost = fields.Str()
    popularity = fields.Int()
    booking_url = fields.Str()

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

class UserRoadmapProgressSchema(Schema):
    progress_id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    roadmap_id = fields.Int(required=True)
    node_id = fields.Int(required=True)
    status = fields.Str()
    started_at = fields.DateTime(allow_none=True)
    completed_at = fields.DateTime(allow_none=True)

class FavoriteSchema(Schema):
    favorite_id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    location_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
