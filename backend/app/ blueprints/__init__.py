from .hobbies import hobby_bp
from .users import user_bp
from .locations import location_bp
from .roadmaps import roadmap_bp

def register_blueprints(app):
    app.register_blueprint(hobby_bp, url_prefix='/api/hobbies')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(location_bp, url_prefix='/api/locations')
    app.register_blueprint(roadmap_bp, url_prefix='/api/roadmaps')