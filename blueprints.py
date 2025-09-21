from routes.auth_routes import auth_bp
from routes.plan_routes import plan_bp
from routes.plan_feature_routes import feature_bp 
from routes.plan_promotion_routes import plan_promo_bp 
from routes.plan_channel_routes import plan_channel_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.customer_routes import customer_bp
from routes.address_routes import address_bp
from routes.payment_routes import payment_bp
from routes.comment_routes import comment_bp
from routes.inventory_routes import inventory_bp
from routes.order_routes import order_bp
from routes.coupon_routes import coupon_bp
from routes.gallery_routes import gallery_bp
from routes.offer_routes import offer_bp
from routes.supplier_routes import supplier_bp
from routes.customer_types_routes import customer_types_routes
#imports

def register_blueprints(app):
    app.register_blueprint(plan_bp)
    app.register_blueprint(feature_bp)
    app.register_blueprint(plan_promo_bp)
    app.register_blueprint(plan_channel_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(coupon_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(offer_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(customer_types_routes)
    