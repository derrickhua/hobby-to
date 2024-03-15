from datetime import datetime
from .database import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Hobby(db.Model):
    __tablename__ = 'hobbies'
    hobby_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(255), nullable=False)
    sub_category = db.Column(db.String(255), nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    cost = db.Column(db.String(255))
    popularity = db.Column(db.Integer)
    booking_url = db.Column(db.String(255))


class HobbyLocation(db.Model):
    __tablename__ = 'hobby_location'
    hobby_location_id = db.Column(db.Integer, primary_key=True)  # Adjusted column name
    hobby_id = db.Column(db.Integer, db.ForeignKey('hobbies.hobby_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)

class Roadmap(db.Model):
    __tablename__ = 'roadmaps'
    roadmap_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    hobby_id = db.Column(db.Integer, db.ForeignKey('hobbies.hobby_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RoadmapNode(db.Model):
    __tablename__ = 'roadmap_nodes'
    node_id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.roadmap_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    parent_node_id = db.Column(db.Integer, db.ForeignKey('roadmap_nodes.node_id'), nullable=True)
    estimated_time = db.Column(db.String(255))

class UserHobbies(db.Model):
    __tablename__ = 'user_hobbies'
    user_hobby_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    hobby_id = db.Column(db.Integer, db.ForeignKey('hobbies.hobby_id'), nullable=False)
    status = db.Column(db.String(255))
    progress_notes = db.Column(db.Text)

class UserRoadmapProgress(db.Model):
    __tablename__ = 'user_roadmap_progress'
    progress_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.roadmap_id'), nullable=False)
    node_id = db.Column(db.Integer, db.ForeignKey('roadmap_nodes.node_id'), nullable=False)
    status = db.Column(db.String(255))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
