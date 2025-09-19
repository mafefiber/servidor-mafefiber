from routes.auth_routes import auth_bp
from routes.plan_routes import plan_bp
from routes.plan_feature_routes import feature_bp 
from routes.plan_promotion_routes import plan_promo_bp 
from routes.plan_channel_routes import plan_channel_bp


#imports

def register_blueprints(app):
    app.register_blueprint(plan_bp)
    app.register_blueprint(feature_bp)
    app.register_blueprint(plan_promo_bp)
    app.register_blueprint(plan_channel_bp)
    app.register_blueprint(auth_bp)