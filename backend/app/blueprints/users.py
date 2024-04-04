from flask import Blueprint, request, jsonify, current_app, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db
from marshmallow import ValidationError
from ..models import User, Hobby, UserHobbies, UserRoadmapProgress, Favorite
from ..schemas import UserSchema, UserHobbySchema, UserRoadmapProgressSchema, FavoriteSchema
from sqlalchemy.exc import SQLAlchemyError
from ..limiter import limiter

user_bp = Blueprint('user_bp', __name__)
users_bp = Blueprint('users_bp', __name__)
user_roadmap_progress_schema = UserRoadmapProgressSchema(many=True)

@users_bp.route('/api/users/register', methods=['POST'])
@limiter.limit("10 per hour")
def register_user():
    user_schema = UserSchema()
    data = request.get_json()
    errors = user_schema.validate(data, partial=("user_id", "created_at"))
    if errors:
        current_app.logger.warning('Validation errors in registration attempt')
        return jsonify(errors), 400

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        current_app.logger.warning(f"Email already exists: {email}")
        return jsonify({'message': 'Email already registered'}), 409

    try:
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"User registered: {email}")
        return jsonify({'message': 'User registered successfully', 'user': user_schema.dump(new_user, exclude=['password_hash'])}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to register user: {e}")
        return jsonify({'message': 'Failed to register user'}), 500

@users_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        current_app.logger.warning('Missing email or password in login attempt')
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        current_app.logger.warning(f"User not found for email: {email}")
        return jsonify({"message": "Email not registered"}), 404

    if check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.user_id)
        current_app.logger.info(f"User logged in: {email}")
        
        response = make_response(jsonify({"message": "Login successful"}), 200)
        response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
        return response
    else:
        current_app.logger.warning(f'Invalid login attempt for email: {email}')
        return jsonify({"message": "Invalid email or password"}), 401

@users_bp.route('/logout', methods=['POST'])
def logout_user():
    response = make_response(jsonify({"message": "Logged out successfully"}), 200)
    response.set_cookie('access_token', '', httponly=True, expires=0)  
    return response

@users_bp.route('/api/users/<int:user_id>/dashboard', methods=['GET'])
@jwt_required()
def user_dashboard(user_id):
    current_user_id = get_jwt_identity()
    if user_id != current_user_id:
        current_app.logger.warning(f"Unauthorized access attempt to user dashboard: {user_id}")
        return jsonify({"message": "Access unauthorized"}), 403

    try:
        # Assuming you have a method to fetch dashboard data
        # dashboard_data = get_dashboard_data(user_id)
        # Placeholder response
        dashboard_data = {"message": "This is your dashboard data"}

        current_app.logger.info(f"User {user_id} accessed their dashboard")
        return jsonify(dashboard_data), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching dashboard for user {user_id}: {e}")
        return jsonify({"message": "Failed to fetch dashboard data"}), 500


@users_bp.route('/api/user_hobbies', methods=['POST'])
@jwt_required()
def add_user_hobby():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    user_hobby_schema = UserHobbySchema()  
    errors = user_hobby_schema.validate(data)  

    if errors:
        current_app.logger.warning(f"Validation errors: {errors}")
        return jsonify(errors), 400

    hobby_id = data['hobby_id']
    if not Hobby.query.get(hobby_id):
        current_app.logger.warning(f"Hobby ID {hobby_id} not found")
        return jsonify({'message': 'Hobby not found'}), 404

    try:
        new_user_hobby = UserHobbies(user_id=current_user_id, **data)  
        db.session.add(new_user_hobby)
        db.session.commit()
        current_app.logger.info(f"User {current_user_id} added hobby {hobby_id}")
        
        return jsonify({'message': 'Hobby added to user profile successfully', 'user_hobby': user_hobby_schema.dump(new_user_hobby)}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding hobby {hobby_id} to user {current_user_id}: {e}")
        return jsonify({'message': 'Failed to add hobby to user profile'}), 500

@users_bp.route('/api/users/<int:user_id>/hobbies', methods=['GET'])
@jwt_required()
def get_user_hobbies(user_id):
    current_user_id = get_jwt_identity()
    if user_id != current_user_id:
        current_app.logger.warning('Unauthorized access attempt')
        return jsonify({'message': 'Access unauthorized'}), 403

    try:
        user_hobbies = UserHobbies.query.filter_by(user_id=user_id).all()
        user_hobbies_schema = UserHobbySchema(many=True)
        hobbies_data = user_hobbies_schema.dump(user_hobbies)
        return jsonify(hobbies_data), 200
    except Exception as e:
        current_app.logger.error(f"Failed to fetch hobbies for user {user_id}: {e}")
        return jsonify({'message': 'Failed to fetch hobbies'}), 500

    
@users_bp.route('/api/user_roadmap_progress', methods=['POST'])
@jwt_required()
def add_user_roadmap_progress():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    schema = UserRoadmapProgressSchema()
    
    try:
        validated_data = schema.load(data)
        validated_data['user_id'] = current_user_id
        new_progress = UserRoadmapProgress(**validated_data)
        db.session.add(new_progress)
        db.session.commit()
        return jsonify({'message': 'Roadmap progress added successfully', 'progress': schema.dump(new_progress)}), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding roadmap progress for user {current_user_id}: {e}")
        return jsonify({'message': 'Failed to add roadmap progress'}), 500

@users_bp.route('/api/users/<int:user_id>/roadmap_progress', methods=['GET'])
@jwt_required()
def get_user_roadmap_progress(user_id):
    current_user_id = get_jwt_identity()
    if user_id != current_user_id:
        current_app.logger.warning(f"Unauthorized access attempt to user's roadmap progress: {user_id}")
        return jsonify({"message": "Access unauthorized"}), 403
    
    try:
        progress_items = UserRoadmapProgress.query.filter_by(user_id=user_id).all()
        progress_data = user_roadmap_progress_schema.dump(progress_items)
        return jsonify(progress_data), 200
    except Exception as e:
        current_app.logger.error(f"Failed to fetch roadmap progress for user {user_id}: {e}")
        return jsonify({"message": "Failed to fetch roadmap progress"}), 500

@users_bp.route('/api/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    schema = FavoriteSchema()
    
    try:
        validated_data = schema.load(data)
        validated_data['user_id'] = current_user_id
        new_favorite = Favorite(**validated_data)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({'message': 'Added to favorites successfully', 'favorite': schema.dump(new_favorite)}), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding to favorites for user {current_user_id}: {e}")
        return jsonify({'message': 'Failed to add to favorites'}), 500

@users_bp.route('/api/users/<int:user_id>/favorites', methods=['GET'])
@jwt_required()
def get_user_favorites(user_id):
    current_user_id = get_jwt_identity()
    if user_id != current_user_id:
        current_app.logger.warning(f"Unauthorized access attempt to user's favorites: {user_id}")
        return jsonify({"message": "Access unauthorized"}), 403
    
    try:
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        schema = FavoriteSchema(many=True)
        return jsonify(schema.dump(favorites)), 200
    except Exception as e:
        current_app.logger.error(f"Failed to fetch favorites for user {user_id}: {e}")
        return jsonify({"message": "Failed to fetch favorites"}), 500
