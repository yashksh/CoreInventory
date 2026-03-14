"""
CoreInventory — Database Models
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ─────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.login_id}>"


# ─────────────────────────────────────────────
# CONTACTS
# ─────────────────────────────────────────────
class Contact(db.Model):

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), default='vendor')
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Contact {self.name}>"


# ─────────────────────────────────────────────
# PRODUCTS
# ─────────────────────────────────────────────
class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    unit_cost = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    inventory_entries = db.relationship('Inventory', backref='product', lazy='dynamic')

    def __repr__(self):
        return f"<Product {self.product_code}>"


# ─────────────────────────────────────────────
# WAREHOUSES
# ─────────────────────────────────────────────
class Warehouse(db.Model):

    __tablename__ = "warehouses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    locations = db.relationship('Location', backref='warehouse', lazy='dynamic')

    def __repr__(self):
        return f"<Warehouse {self.short_code}>"


# ─────────────────────────────────────────────
# LOCATIONS
# ─────────────────────────────────────────────
class Location(db.Model):

    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    short_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Location {self.short_code}>"


# ─────────────────────────────────────────────
# INVENTORY
# ─────────────────────────────────────────────
class Inventory(db.Model):

    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    quantity = db.Column(db.Integer, default=0)

    location = db.relationship('Location', backref='inventory_entries')

    __table_args__ = (
        db.UniqueConstraint('product_id', 'location_id'),
    )

    def __repr__(self):
        return f"<Inventory product={self.product_id} loc={self.location_id} qty={self.quantity}>"


# ─────────────────────────────────────────────
# STOCK MOVES (Receipts / Deliveries / Internal)
# ─────────────────────────────────────────────
class StockMove(db.Model):

    __tablename__ = "stock_moves"

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(30), unique=True, nullable=False)
    operation_type = db.Column(db.String(20), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"))
    from_location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    to_location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    schedule_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='draft')
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    contact = db.relationship('Contact', backref='stock_moves')
    from_location = db.relationship('Location', foreign_keys=[from_location_id], backref='moves_from')
    to_location = db.relationship('Location', foreign_keys=[to_location_id], backref='moves_to')
    creator = db.relationship('User', backref='stock_moves')
    lines = db.relationship('StockMoveLine', backref='move', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<StockMove {self.reference} ({self.status})>"


# ─────────────────────────────────────────────
# STOCK MOVE LINES
# ─────────────────────────────────────────────
class StockMoveLine(db.Model):

    __tablename__ = "stock_move_lines"

    id = db.Column(db.Integer, primary_key=True)
    move_id = db.Column(db.Integer, db.ForeignKey("stock_moves.id", ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', backref='move_lines')

    def __repr__(self):
        return f"<StockMoveLine move={self.move_id} product={self.product_id} qty={self.quantity}>"


# ─────────────────────────────────────────────
# MOVE HISTORY
# ─────────────────────────────────────────────
class MoveHistory(db.Model):

    __tablename__ = "move_history"

    id = db.Column(db.Integer, primary_key=True)
    move_id = db.Column(db.Integer, db.ForeignKey("stock_moves.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    from_location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    to_location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    quantity = db.Column(db.Integer, nullable=False)
    move_date = db.Column(db.DateTime, server_default=db.func.now())

    move = db.relationship('StockMove', backref='history')
    product = db.relationship('Product', backref='move_history')
    from_location = db.relationship('Location', foreign_keys=[from_location_id])
    to_location = db.relationship('Location', foreign_keys=[to_location_id])

    def __repr__(self):
        return f"<MoveHistory move={self.move_id} product={self.product_id}>"


# ─────────────────────────────────────────────
# PASSWORD RESET TOKENS (OTP)
# ─────────────────────────────────────────────
class PasswordResetToken(db.Model):

    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='reset_tokens')

    def is_expired(self):
        from datetime import datetime
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f"<PasswordResetToken user={self.user_id} used={self.used}>"