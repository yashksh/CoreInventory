"""
CoreInventory — Settings Routes
Manage warehouses, locations, and contacts (shared company-wide data).
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import db, Warehouse, Location, Contact

settings_bp = Blueprint('settings', __name__)


def require_login():
    return 'user_id' in session


# ─────────────────────────────────────────────
# SETTINGS PAGE
# ─────────────────────────────────────────────
@settings_bp.route('/settings')
def settings_page():
    if not require_login():
        return redirect(url_for('auth.login'))

    warehouses = Warehouse.query.order_by(Warehouse.id).all()
    locations = Location.query.order_by(Location.id).all()
    contacts = Contact.query.order_by(Contact.id).all()

    return render_template(
        'settings.html',
        warehouses=warehouses,
        locations=locations,
        contacts=contacts,
    )


# ═══════════════════════════════════════════════
# WAREHOUSES
# ═══════════════════════════════════════════════

@settings_bp.route('/api/warehouse/add', methods=['POST'])
def api_add_warehouse():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    name = (data.get('name') or '').strip()
    short_code = (data.get('short_code') or '').strip()
    address = (data.get('address') or '').strip()

    if not name or not short_code:
        return jsonify({'success': False, 'error': 'Name and short code required'}), 400

    if Warehouse.query.filter_by(short_code=short_code).first():
        return jsonify({'success': False, 'error': 'Short code already exists'}), 409

    wh = Warehouse(name=name, short_code=short_code, address=address)
    db.session.add(wh)
    db.session.commit()
    return jsonify({'success': True, 'id': wh.id})


@settings_bp.route('/api/warehouse/update', methods=['POST'])
def api_update_warehouse():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    wh = Warehouse.query.get(data.get('id'))
    if not wh:
        return jsonify({'success': False, 'error': 'Not found'}), 404

    name = (data.get('name') or '').strip()
    if name:
        wh.name = name
    wh.address = (data.get('address') or '').strip()
    db.session.commit()
    return jsonify({'success': True})


@settings_bp.route('/api/warehouse/delete', methods=['POST'])
def api_delete_warehouse():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    wh = Warehouse.query.get(data.get('id'))
    if not wh:
        return jsonify({'success': False, 'error': 'Not found'}), 404

    db.session.delete(wh)
    db.session.commit()
    return jsonify({'success': True})


# ═══════════════════════════════════════════════
# LOCATIONS
# ═══════════════════════════════════════════════

@settings_bp.route('/api/location/add', methods=['POST'])
def api_add_location():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    warehouse_id = data.get('warehouse_id')
    name = (data.get('name') or '').strip()
    short_code = (data.get('short_code') or '').strip()

    if not warehouse_id or not name or not short_code:
        return jsonify({'success': False, 'error': 'All fields required'}), 400

    loc = Location(warehouse_id=warehouse_id, name=name, short_code=short_code)
    db.session.add(loc)
    db.session.commit()
    return jsonify({'success': True, 'id': loc.id})


@settings_bp.route('/api/location/update', methods=['POST'])
def api_update_location():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    loc = Location.query.get(data.get('id'))
    if not loc:
        return jsonify({'success': False, 'error': 'Not found'}), 404

    name = (data.get('name') or '').strip()
    if name:
        loc.name = name
    db.session.commit()
    return jsonify({'success': True})


@settings_bp.route('/api/location/delete', methods=['POST'])
def api_delete_location():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    loc = Location.query.get(data.get('id'))
    if not loc:
        return jsonify({'success': False, 'error': 'Not found'}), 404

    db.session.delete(loc)
    db.session.commit()
    return jsonify({'success': True})


# ═══════════════════════════════════════════════
# CONTACTS
# ═══════════════════════════════════════════════

@settings_bp.route('/api/contact/add', methods=['POST'])
def api_add_contact():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    name = (data.get('name') or '').strip()
    ctype = data.get('type', 'vendor')
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()

    if not name:
        return jsonify({'success': False, 'error': 'Name required'}), 400

    c = Contact(name=name, type=ctype, email=email or None, phone=phone or None)
    db.session.add(c)
    db.session.commit()
    return jsonify({'success': True, 'id': c.id})


@settings_bp.route('/api/contact/update', methods=['POST'])
def api_update_contact():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    c = Contact.query.get(data.get('id'))
    if not c:
        return jsonify({'success': False, 'error': 'Not found'}), 404

    name = (data.get('name') or '').strip()
    if name:
        c.name = name
    c.type = data.get('type', c.type)
    c.email = (data.get('email') or '').strip() or None
    c.phone = (data.get('phone') or '').strip() or None
    db.session.commit()
    return jsonify({'success': True})


@settings_bp.route('/api/contact/delete', methods=['POST'])
def api_delete_contact():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    c = Contact.query.get(data.get('id'))
    if not c:
        return jsonify({'success': False, 'error': 'Not found'}), 404

    db.session.delete(c)
    db.session.commit()
    return jsonify({'success': True})
