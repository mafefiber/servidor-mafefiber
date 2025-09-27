from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()
#table users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(208), nullable=False)
    full_name = db.Column(db.String(120))
    id_admin = db.Column(db.Boolean, default=False)
    is_active= db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


#table tokens

class UserToken(db.Model):
    __tablename__ = 'user_tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)  # Activado/desactivado
    
    user = db.relationship('User', backref=db.backref('tokens', lazy=True))

#table customer
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # PK y FK
    customer_type_id = db.Column(db.Integer, db.ForeignKey('customer_types.id'), nullable=False, default=3)
    is_active = db.Column(db.Boolean, default=True)
    create_at = db.Column(db.DateTime, server_default=db.func.now())
    
    user = db.relationship('User', backref=db.backref('customer', uselist=False))

#table customer types
class CustomerType(db.Model):
    __tablename__='customer_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Example: 'individual', 'company'
    description = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    create_at = db.Column(db.DateTime, server_default=db.func.now())

#table persons
class Person(db.Model):
    __tablename__ = 'persons'
    id= db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # Example: 'DNI', 'Passport'
    document_number = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    customer = db.relationship('Customer', backref=db.backref('persons', uselist=False))

#table companies
class Company(db.Model):
    __tablename__= 'companies'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    business_name = db.Column(db.String(120), nullable=False)
    tax_id = db.Column(db.String(50), unique=True, nullable=False)  # Example: 'RUC', 'Tax ID'
    contact_name = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    customer = db.relationship('Customer', backref=db.backref('company', uselist=False))

#tables addres(db.Model):
class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    address_line = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), nullable=False)
    reference = db.Column(db.String(200))  #additional reference
    is_default = db.Column(db.Boolean, default=False)  #default address
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    customer = db.relationship('Customer', backref=db.backref('addresses', lazy=True))

#table plans
class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    speed_mbps = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    technology = db.Column(db.String(50), nullable=False)  # Example: 'fibra', 'radioenlace', 'cable'
    description = db.Column(db.Text)
    features = db.Column(db.Text,nullable=True)  # <-- aquí puedes guardar una lista o dict de características
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

#table plan features
class PlanFeature(db.Model):
    __tablename__='plan_features'
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    feature = db.Column(db.String(120), nullable=False)  # Example: 'Instalación gratuita', 'Router incluido', 'Soporte técnico', 'Canales HD'
    value = db.Column(db.String(120))  # additional value if applicable (ej: 'Lunes a sábado de 8am a 6pm')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    plan = db.relationship('Plan', backref=db.backref('plan_features', lazy=True))
#table subscriptions
class Subscription(db.Model):
    __tablename__='subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), nullable=False)  # Example: 'active
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    customer = db.relationship('Customer', backref=db.backref('subscriptions', lazy=True))
    plan = db.relationship('Plan', backref=db.backref('subscriptions', lazy=True))

#table promotions
class Promotions(db.Model):
    __tablename__ = 'promotions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    discount_percent = db.Column(db.Integer)  # Porcentaje de descuento
    valid_from = db.Column(db.DateTime)
    valid_to = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

#table plan promotions
class PlanPromotion(db.Model):
    __tablename__ = 'plan_promotions'
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    plan = db.relationship('Plan', backref=db.backref('plan_promotions', lazy=True))
    promotion = db.relationship('Promotions', backref=db.backref('plan_promotions', lazy=True))

#table serviceRequest

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    request_type = db.Column(db.String(50), nullable=False)  # Example: 'installation', 'repair', 'upgrade'
    description = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False)  # Example: 'pending', 'in_progress', 'completed'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    customer = db.relationship('Customer', backref=db.backref('service_requests', lazy=True))
    subscription = db.relationship('Subscription', backref=db.backref('service_requests', lazy=True))

#table products
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10,2), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)  # Stock Keeping Unit
    stock_quantity = db.Column(db.Integer, default=0) # Quantity in stock
    is_active = db.Column(db.Boolean, default=True)
    create_at=db.Column(db.DateTime, server_default=db.func.now())
    images = db.Column(db.Text, nullable=True)  # image urls separated by line breaks


#table commets
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Who made the comment
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # Optional rating (1-5)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    customer = db.relationship('Customer', backref=db.backref('comments', lazy=True))
    subscription = db.relationship('Subscription', backref=db.backref('comments', lazy=True))
    product = db.relationship('Product', backref=db.backref('comments', lazy=True))
    plan = db.relationship('Plan', backref=db.backref('comments', lazy=True))
    service_request = db.relationship('ServiceRequest', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

#table oreders
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Who created the order
    total_amount = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Example: 'pending', 'completed', 'canceled'
    payment_method = db.Column(db.String(50))  # Example: 'credit_card', 'paypal', 'bank_transfer'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

#table order items
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10,2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))
    plan = db.relationship('Plan', backref=db.backref('order_items', lazy=True))

#table inventory
class Inventory(db.Model):
   __tablename__ = 'inventory'
   id = db.Column(db.Integer, primary_key=True)
   product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
   warehouse = db.Column(db.String(100), nullable=False)  # Example: 'Main Warehouse', 'Secondary Warehouse'
   quantity = db.Column(db.Integer, nullable=False, default=0)
   is_active = db.Column(db.Boolean, default=True)
   updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

   product = db.relationship('Product', backref=db.backref('inventory', lazy=True))

#table payments
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    payment_date = db.Column(db.DateTime,server_default=db.func.now())
    payment_method = db.Column(db.String(50), nullable=False)  # Example: 'credit_card', 'paypal', 'bank_transfer'
    reference = db.Column(db.String(100))  # Transaction reference or ID number operation
    status = db.Column(db.String(50), nullable=False)  # Example: 'completed', 'pending', 'failed'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    order = db.relationship('Order', backref=db.backref('payments', lazy=True))
    subscription = db.relationship('Subscription', backref=db.backref('payments', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('payments', lazy=True))

#payment_gateway
class PaymentGateway(db.Model):
    __tablename__= 'payment_gateways'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Example: 'Stripe', 'PayPal'
    api_key = db.Column(db.String(256), nullable=False)
    api_url = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

#table payment transactions
class PaymentTransaction(db.Model):
    __tablename__ = 'payment_transactions'
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    gateway_id = db.Column(db.Integer, db.ForeignKey('payment_gateways.id'), nullable=False)
    transaction_id = db.Column(db.String(120), nullable=False)  # ID de la transacción en la pasarela
    status = db.Column(db.String(50), nullable=False)  # Ejemplo: 'pending', 'completed', 'failed'
    amount = db.Column(db.Numeric(10,2), nullable=False)
    response_data = db.Column(db.Text)  # JSON o texto con la respuesta de la pasarela
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    payment = db.relationship('Payment', backref=db.backref('transactions', lazy=True))
    gateway = db.relationship('PaymentGateway', backref=db.backref('transactions', lazy=True))

#table coupons
class Coupon(db.Model):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    discount_type = db.Column(db.String(20), nullable=False)  # 'percent' o 'amount'
    discount_value = db.Column(db.Numeric(10,2), nullable=False)
    valid_from = db.Column(db.DateTime)
    valid_to = db.Column(db.DateTime)
    usage_limit = db.Column(db.Integer)  # Número máximo de usos
    used_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

#table order_coupons
class OrderCoupon(db.Model):
    __tablename__ = 'order_coupons'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable=False)
    discount_amount = db.Column(db.Numeric(10,2), nullable=False)
    applied_at = db.Column(db.DateTime, server_default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)

    order = db.relationship('Order', backref=db.backref('order_coupons', lazy=True))
    coupon = db.relationship('Coupon', backref=db.backref('order_coupons', lazy=True))

#table offers
class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    discount_type = db.Column(db.String(20), nullable=False)  # 'percent' o 'amount'
    discount_value = db.Column(db.Numeric(10,2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

#table marketing_campaigns
class MarketingCampaign(db.Model):
    __tablename__ = 'marketing_campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Numeric(12,2))
    channel = db.Column(db.String(100))  # Ejemplo: 'email', 'social', 'sms'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

#table logs
class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(120), nullable=False)  # Ejemplo: 'login', 'create_order', 'update_product'
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))  # IPv4/IPv6
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref=db.backref('logs', lazy=True))

#table cash_register_sessions
class CashRegisterSession(db.Model):
    __tablename__ = 'cash_register_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opening_amount = db.Column(db.Numeric(10,2), nullable=False)
    closing_amount = db.Column(db.Numeric(10,2))
    opened_at = db.Column(db.DateTime, server_default=db.func.now())
    closed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), nullable=False, default='open')  # 'open', 'closed', 'discrepancy'
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref=db.backref('cash_register_sessions', lazy=True))

#table cash_movements
class CashMovement(db.Model):
    __tablename__ = 'cash_movements'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('cash_register_sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movement_type = db.Column(db.String(50), nullable=False)  # 'income', 'expense', 'transfer'
    amount = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.Text)
    related_payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)

    session = db.relationship('CashRegisterSession', backref=db.backref('cash_movements', lazy=True))
    user = db.relationship('User', backref=db.backref('cash_movements', lazy=True))
    payment = db.relationship('Payment', backref=db.backref('cash_movements', lazy=True))

    #table cash_discrepancies
class CashDiscrepancy(db.Model):
    __tablename__ = 'cash_discrepancies'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('cash_register_sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expected_amount = db.Column(db.Numeric(10,2), nullable=False)
    actual_amount = db.Column(db.Numeric(10,2), nullable=False)
    discrepancy_amount = db.Column(db.Numeric(10,2), nullable=False)
    reason = db.Column(db.Text)
    resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    session = db.relationship('CashRegisterSession', backref=db.backref('cash_discrepancies', lazy=True))
    user = db.relationship('User', backref=db.backref('cash_discrepancies', lazy=True))

#table channels
class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

#table plan_channels
class PlanChannel(db.Model):
    __tablename__ = 'plan_channels'
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    plan = db.relationship('Plan', backref=db.backref('plan_channels', lazy=True))
    channel = db.relationship('Channel', backref=db.backref('plan_channels', lazy=True))

#table tickets
class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Usuario que atiende el ticket
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False)  # 'open', 'in_progress', 'closed'
    priority = db.Column(db.String(20))  # 'low', 'medium', 'high'
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    closed_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    customer = db.relationship('Customer', backref=db.backref('tickets', lazy=True))
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))

    #table suppliers
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact_name = db.Column(db.String(120))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    tax_id = db.Column(db.String(50), unique=True)  # Ejemplo: RUC, Tax ID
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

#table product_purchases
class ProductPurchase(db.Model):
    __tablename__ = 'product_purchases'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10,2), nullable=False)
    total_price = db.Column(db.Numeric(10,2), nullable=False)
    purchase_date = db.Column(db.DateTime, server_default=db.func.now())
    invoice_number = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    supplier = db.relationship('Supplier', backref=db.backref('product_purchases', lazy=True))
    product = db.relationship('Product', backref=db.backref('product_purchases', lazy=True))

#table inventory_movements
class InventoryMovement(db.Model):
    __tablename__ = 'inventory_movements'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse = db.Column(db.String(100), nullable=False)
    movement_type = db.Column(db.String(50), nullable=False)  # 'in', 'out', 'transfer', etc.
    quantity = db.Column(db.Integer, nullable=False)
    related_purchase_id = db.Column(db.Integer, db.ForeignKey('product_purchases.id'), nullable=True)
    related_order_item_id = db.Column(db.Integer, db.ForeignKey('order_items.id'), nullable=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)

    product = db.relationship('Product', backref=db.backref('inventory_movements', lazy=True))
    purchase = db.relationship('ProductPurchase', backref=db.backref('inventory_movements', lazy=True))
    order_item = db.relationship('OrderItem', backref=db.backref('inventory_movements', lazy=True))

#table PasswordResets
class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('password_reset_tokens', lazy=True))

#gallery images
class GalleryImage(db.Model):
    __tablename__ = 'gallery_images'
    id = db.Column(db.Integer, primary_key=True)
    urls = db.Column(db.Text, nullable=False)
    alt_text = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())