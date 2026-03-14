"""
CoreInventory — Stock & Product Routes
Products and inventory are shared company-wide.
Reserved qty is calculated from the logged-in user's pending moves.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from sqlalchemy import func
from models import db, Product, Inventory, Location, StockMove, StockMoveLine

stock_bp = Blueprint('stock', __name__)

PER_PAGE = 10


def require_login():
    return 'user_id' in session


def get_reserved_qty(product_id):
    """Reserved = sum of pending move lines for this product (user-scoped)."""
    uid = session.get('user_id')
    result = (
        db.session.query(func.coalesce(func.sum(StockMoveLine.quantity), 0))
        .join(StockMove, StockMove.id == StockMoveLine.move_id)
        .filter(
            StockMoveLine.product_id == product_id,
            StockMove.status != 'done',
            StockMove.created_by == uid
        )
        .scalar()
    )
    return int(result)


def build_product_rows(products):
    rows = []
    for p in products:
        on_hand = int(
            db.session.query(func.coalesce(func.sum(Inventory.quantity), 0))
            .filter(Inventory.product_id == p.id)
            .scalar()
        )
        reserved = get_reserved_qty(p.id)
        free = max(on_hand - reserved, 0)

        rows.append({
            "id": p.id,
            "product_code": p.product_code,
            "name": p.name,
            "unit_cost": float(p.unit_cost or 0),
            "on_hand": on_hand,
            "reserved": reserved,
            "free_to_use": free
        })
    return rows


def get_summary_stats():
    uid = session.get('user_id')
    all_products = Product.query.all()

    low_stock = 0
    total_value = 0

    for p in all_products:
        on_hand = int(
            db.session.query(func.coalesce(func.sum(Inventory.quantity), 0))
            .filter(Inventory.product_id == p.id)
            .scalar()
        )
        if on_hand < 15:
            low_stock += 1
        total_value += float(p.unit_cost or 0) * on_hand

    reserved_stock = int(
        db.session.query(func.coalesce(func.sum(StockMoveLine.quantity), 0))
        .join(StockMove, StockMove.id == StockMoveLine.move_id)
        .filter(StockMove.status != "done", StockMove.created_by == uid)
        .scalar()
    )

    if total_value >= 1_000_000:
        value_display = f"{total_value/1_000_000:.1f}M"
    elif total_value >= 1000:
        value_display = f"{total_value/1000:.0f}k"
    else:
        value_display = f"{total_value:.0f}"

    return low_stock, value_display, reserved_stock


# ─────────────────────────────────────────────
# STOCK PAGE
# ─────────────────────────────────────────────
@stock_bp.route("/stock")
def stock_page():
    if not require_login():
        return redirect(url_for("auth.login"))

    page = request.args.get("page", 1, type=int)
    search_q = request.args.get("q", "").strip()

    query = Product.query
    if search_q:
        like = f"%{search_q}%"
        query = query.filter(
            (Product.name.ilike(like)) | (Product.product_code.ilike(like))
        )

    total_products = query.count()
    products = query.order_by(Product.id).offset((page-1)*PER_PAGE).limit(PER_PAGE).all()
    rows = build_product_rows(products)
    low_stock, inv_value, reserved = get_summary_stats()
    locations = Location.query.all()
    total_pages = max((total_products + PER_PAGE - 1) // PER_PAGE, 1)

    return render_template(
        "stock.html",
        products=rows,
        total_products=total_products,
        page=page,
        per_page=PER_PAGE,
        total_pages=total_pages,
        search_q=search_q,
        low_stock_items=low_stock,
        inventory_value=inv_value,
        reserved_stock=reserved,
        locations=locations
    )


# ─────────────────────────────────────────────
# API: PRODUCTS LIST
# ─────────────────────────────────────────────
@stock_bp.route("/api/products")
def api_products():
    if not require_login():
        return jsonify({"error": "not logged in"}), 401

    rows = build_product_rows(Product.query.all())
    low_stock, inv_value, reserved = get_summary_stats()
    return jsonify({
        "products": rows, "total": len(rows),
        "low_stock_items": low_stock,
        "inventory_value": inv_value,
        "reserved_stock": reserved
    })


# ─────────────────────────────────────────────
# API: SEARCH PRODUCTS
# ─────────────────────────────────────────────
@stock_bp.route("/api/products/search")
def api_products_search():
    if not require_login():
        return jsonify({"error": "not logged in"}), 401

    search_q = request.args.get("q", "").strip()
    query = Product.query
    if search_q:
        like = f"%{search_q}%"
        query = query.filter(
            (Product.name.ilike(like)) | (Product.product_code.ilike(like))
        )

    products = query.order_by(Product.id).all()
    rows = build_product_rows(products)
    low_stock, inv_value, reserved = get_summary_stats()
    return jsonify({
        "products": rows, "total": len(rows),
        "low_stock_items": low_stock,
        "inventory_value": inv_value,
        "reserved_stock": reserved
    })


# ─────────────────────────────────────────────
# ADD PRODUCT
# ─────────────────────────────────────────────
@stock_bp.route("/api/product/add", methods=["POST"])
def api_add_product():
    if not require_login():
        return jsonify({"error": "not logged in"}), 401

    data = request.get_json()
    product_code = (data.get("product_code") or "").strip()
    name = (data.get("name") or "").strip()
    unit_cost = float(data.get("unit_cost") or 0)

    if not product_code or not name:
        return jsonify({"success": False, "error": "Product code and name required"}), 400

    if Product.query.filter_by(product_code=product_code).first():
        return jsonify({"success": False, "error": "Product code already exists"}), 409

    product = Product(product_code=product_code, name=name, unit_cost=unit_cost)
    db.session.add(product)
    db.session.commit()
    return jsonify({"success": True, "product_id": product.id})


# ─────────────────────────────────────────────
# UPDATE PRODUCT
# ─────────────────────────────────────────────
@stock_bp.route("/api/product/update", methods=["POST"])
def api_update_product():
    if not require_login():
        return jsonify({"error": "not logged in"}), 401

    data = request.get_json()
    product = Product.query.get(data.get("product_id"))
    if not product:
        return jsonify({"success": False, "error": "Product not found"}), 404

    name = (data.get("name") or "").strip()
    if name:
        product.name = name
    if data.get("unit_cost") is not None:
        product.unit_cost = float(data["unit_cost"])

    db.session.commit()
    return jsonify({"success": True})


# ─────────────────────────────────────────────
# UPDATE STOCK QTY
# ─────────────────────────────────────────────
@stock_bp.route("/api/stock/update", methods=["POST"])
def api_stock_update():
    if not require_login():
        return jsonify({"error": "not logged in"}), 401

    data = request.get_json()
    product_id = data.get("product_id")
    location_id = data.get("location_id")
    quantity = int(data.get("quantity", 0))

    if not product_id or not location_id:
        return jsonify({"success": False, "error": "Product and location required"}), 400

    inv = Inventory.query.filter_by(
        product_id=product_id, location_id=location_id
    ).first()

    if inv:
        inv.quantity = quantity
    else:
        db.session.add(Inventory(
            product_id=product_id,
            location_id=location_id,
            quantity=quantity
        ))

    db.session.commit()
    return jsonify({"success": True})