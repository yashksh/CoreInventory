"""
CoreInventory — Operations Routes
Handles receipt, delivery, and internal stock move operations.
All data is scoped to the logged-in user via created_by.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import date, datetime
from models import (
    db, StockMove, StockMoveLine, Product, Inventory,
    Location, Contact, MoveHistory
)

operations_bp = Blueprint('operations', __name__)


def require_login():
    return 'user_id' in session


def generate_reference(op_type):
    """Generate a unique reference like WH/IN/00001."""
    prefix_map = {
        'receipt': 'WH/IN/',
        'delivery': 'WH/OUT/',
        'internal': 'WH/INT/',
    }
    prefix = prefix_map.get(op_type, 'WH/MISC/')

    last_move = (
        StockMove.query
        .filter(StockMove.reference.like(f"{prefix}%"))
        .order_by(StockMove.id.desc())
        .first()
    )

    if last_move:
        try:
            num = int(last_move.reference.replace(prefix, '')) + 1
        except ValueError:
            num = 1
    else:
        num = 1

    return f"{prefix}{num:05d}"


def serialize_move(m):
    """Convert a StockMove to a dict for JSON / template."""
    return {
        'id': m.id,
        'reference': m.reference,
        'operation_type': m.operation_type,
        'contact_name': m.contact.name if m.contact else '—',
        'from_location': m.from_location.short_code if m.from_location else '—',
        'to_location': m.to_location.short_code if m.to_location else '—',
        'schedule_date': m.schedule_date.strftime('%Y-%m-%d') if m.schedule_date else '—',
        'status': m.status,
        'lines_count': len(m.lines),
        'created_at': m.created_at.strftime('%Y-%m-%d %H:%M') if m.created_at else '—',
    }


# ─────────────────────────────────────────────
# OPERATIONS PAGE
# ─────────────────────────────────────────────
@operations_bp.route('/operations')
def operations_page():
    if not require_login():
        return redirect(url_for('auth.login'))

    uid = session['user_id']
    op_type = request.args.get('type', 'all')

    query = StockMove.query.filter(StockMove.created_by == uid)

    if op_type in ('receipt', 'delivery', 'internal'):
        query = query.filter(StockMove.operation_type == op_type)

    moves = query.order_by(StockMove.created_at.desc()).all()
    rows = [serialize_move(m) for m in moves]

    products = Product.query.order_by(Product.name).all()
    locations = Location.query.all()
    contacts = Contact.query.order_by(Contact.name).all()

    return render_template(
        'operations.html',
        moves=rows,
        current_type=op_type,
        products=products,
        locations=locations,
        contacts=contacts,
    )


# ─────────────────────────────────────────────
# API: LIST OPERATIONS (user-scoped)
# ─────────────────────────────────────────────
@operations_bp.route('/api/operations')
def api_operations():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    uid = session['user_id']
    op_type = request.args.get('type', 'all')
    query = StockMove.query.filter(StockMove.created_by == uid)

    if op_type in ('receipt', 'delivery', 'internal'):
        query = query.filter(StockMove.operation_type == op_type)

    moves = query.order_by(StockMove.created_at.desc()).all()
    rows = [serialize_move(m) for m in moves]

    return jsonify({'operations': rows})


# ─────────────────────────────────────────────
# API: CREATE OPERATION
# ─────────────────────────────────────────────
@operations_bp.route('/api/operation/create', methods=['POST'])
def api_create_operation():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    op_type = data.get('operation_type')

    if op_type not in ('receipt', 'delivery', 'internal'):
        return jsonify({'success': False, 'error': 'Invalid operation type'}), 400

    contact_id = data.get('contact_id') or None
    from_location_id = data.get('from_location_id') or None
    to_location_id = data.get('to_location_id') or None
    schedule_date_str = data.get('schedule_date')
    product_lines = data.get('lines', [])

    if not product_lines:
        return jsonify({'success': False, 'error': 'At least one product line required'}), 400

    schedule_date = None
    if schedule_date_str:
        try:
            schedule_date = datetime.strptime(schedule_date_str, '%Y-%m-%d').date()
        except ValueError:
            schedule_date = date.today()

    reference = generate_reference(op_type)

    move = StockMove(
        reference=reference,
        operation_type=op_type,
        contact_id=contact_id,
        from_location_id=from_location_id,
        to_location_id=to_location_id,
        schedule_date=schedule_date,
        status='draft',
        created_by=session['user_id'],
    )
    db.session.add(move)
    db.session.flush()

    for line in product_lines:
        pid = line.get('product_id')
        qty = int(line.get('quantity', 0))
        if pid and qty > 0:
            db.session.add(StockMoveLine(
                move_id=move.id,
                product_id=pid,
                quantity=qty,
            ))

    db.session.commit()
    return jsonify({'success': True, 'move_id': move.id, 'reference': reference})


# ─────────────────────────────────────────────
# API: CONFIRM (draft → ready)
# ─────────────────────────────────────────────
@operations_bp.route('/api/operation/<int:move_id>/confirm', methods=['POST'])
def api_confirm_operation(move_id):
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    move = StockMove.query.filter_by(id=move_id, created_by=session['user_id']).first()
    if not move:
        return jsonify({'success': False, 'error': 'Operation not found'}), 404

    if move.status not in ('draft', 'waiting'):
        return jsonify({'success': False, 'error': f'Cannot confirm a {move.status} operation'}), 400

    # Delivery: check stock availability
    if move.operation_type == 'delivery' and move.from_location_id:
        for line in move.lines:
            inv = Inventory.query.filter_by(
                product_id=line.product_id,
                location_id=move.from_location_id
            ).first()
            available = inv.quantity if inv else 0
            if available < line.quantity:
                move.status = 'waiting'
                db.session.commit()
                return jsonify({
                    'success': False,
                    'error': f'Insufficient stock for {line.product.name}. Available: {available}, Required: {line.quantity}.'
                }), 400

    move.status = 'ready'
    db.session.commit()
    return jsonify({'success': True, 'status': 'ready'})


# ─────────────────────────────────────────────
# API: VALIDATE (ready → done) — Updates inventory
# ─────────────────────────────────────────────
@operations_bp.route('/api/operation/<int:move_id>/validate', methods=['POST'])
def api_validate_operation(move_id):
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    move = StockMove.query.filter_by(id=move_id, created_by=session['user_id']).first()
    if not move:
        return jsonify({'success': False, 'error': 'Operation not found'}), 404

    if move.status != 'ready':
        return jsonify({'success': False, 'error': f'Cannot validate a {move.status} operation. Confirm first.'}), 400

    for line in move.lines:
        # RECEIPT: increase to_location
        if move.operation_type == 'receipt' and move.to_location_id:
            inv = Inventory.query.filter_by(
                product_id=line.product_id,
                location_id=move.to_location_id
            ).first()
            if inv:
                inv.quantity += line.quantity
            else:
                db.session.add(Inventory(
                    product_id=line.product_id,
                    location_id=move.to_location_id,
                    quantity=line.quantity
                ))

        # DELIVERY: decrease from_location
        elif move.operation_type == 'delivery' and move.from_location_id:
            inv = Inventory.query.filter_by(
                product_id=line.product_id,
                location_id=move.from_location_id
            ).first()
            if inv:
                inv.quantity = max(inv.quantity - line.quantity, 0)

        # INTERNAL: decrease from, increase to
        elif move.operation_type == 'internal':
            if move.from_location_id:
                inv_from = Inventory.query.filter_by(
                    product_id=line.product_id,
                    location_id=move.from_location_id
                ).first()
                if inv_from:
                    inv_from.quantity = max(inv_from.quantity - line.quantity, 0)

            if move.to_location_id:
                inv_to = Inventory.query.filter_by(
                    product_id=line.product_id,
                    location_id=move.to_location_id
                ).first()
                if inv_to:
                    inv_to.quantity += line.quantity
                else:
                    db.session.add(Inventory(
                        product_id=line.product_id,
                        location_id=move.to_location_id,
                        quantity=line.quantity
                    ))

        # Record history
        db.session.add(MoveHistory(
            move_id=move.id,
            product_id=line.product_id,
            from_location_id=move.from_location_id,
            to_location_id=move.to_location_id,
            quantity=line.quantity,
        ))

    move.status = 'done'
    db.session.commit()
    return jsonify({'success': True, 'status': 'done'})


# ─────────────────────────────────────────────
# API: GET OPERATION DETAIL
# ─────────────────────────────────────────────
@operations_bp.route('/api/operation/<int:move_id>')
def api_get_operation(move_id):
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    move = StockMove.query.filter_by(id=move_id, created_by=session['user_id']).first()
    if not move:
        return jsonify({'error': 'not found'}), 404

    lines = [{
        'id': l.id,
        'product_id': l.product_id,
        'product_name': l.product.name if l.product else '—',
        'product_code': l.product.product_code if l.product else '—',
        'quantity': l.quantity,
    } for l in move.lines]

    return jsonify({
        'id': move.id,
        'reference': move.reference,
        'operation_type': move.operation_type,
        'contact_id': move.contact_id,
        'contact_name': move.contact.name if move.contact else '—',
        'from_location_id': move.from_location_id,
        'to_location_id': move.to_location_id,
        'from_location': move.from_location.short_code if move.from_location else '—',
        'to_location': move.to_location.short_code if move.to_location else '—',
        'schedule_date': move.schedule_date.strftime('%Y-%m-%d') if move.schedule_date else '',
        'status': move.status,
        'lines': lines,
    })


# ─────────────────────────────────────────────
# OPERATION DETAIL PAGE
# ─────────────────────────────────────────────
@operations_bp.route('/operations/<int:move_id>')
def operation_detail_page(move_id):
    if not require_login():
        return redirect(url_for('auth.login'))

    move = StockMove.query.filter_by(id=move_id, created_by=session['user_id']).first()
    if not move:
        return redirect(url_for('operations.operations_page'))

    products = Product.query.order_by(Product.name).all()
    locations = Location.query.all()
    contacts = Contact.query.order_by(Contact.name).all()

    return render_template(
        'operation_detail.html',
        move=move,
        products=products,
        locations=locations,
        contacts=contacts,
    )


# ─────────────────────────────────────────────
# CREATE + REDIRECT TO DETAIL PAGE
# ─────────────────────────────────────────────
@operations_bp.route('/operations/new')
def new_operation_redirect():
    if not require_login():
        return redirect(url_for('auth.login'))

    op_type = request.args.get('type', 'receipt')
    if op_type not in ('receipt', 'delivery', 'internal'):
        op_type = 'receipt'

    reference = generate_reference(op_type)

    move = StockMove(
        reference=reference,
        operation_type=op_type,
        schedule_date=date.today(),
        status='draft',
        created_by=session['user_id'],
    )
    db.session.add(move)
    db.session.commit()

    return redirect(url_for('operations.operation_detail_page', move_id=move.id))


# ─────────────────────────────────────────────
# API: CANCEL OPERATION
# ─────────────────────────────────────────────
@operations_bp.route('/api/operation/<int:move_id>/cancel', methods=['POST'])
def api_cancel_operation(move_id):
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    move = StockMove.query.filter_by(id=move_id, created_by=session['user_id']).first()
    if not move:
        return jsonify({'success': False, 'error': 'Operation not found'}), 404

    if move.status == 'done':
        return jsonify({'success': False, 'error': 'Cannot cancel a completed operation'}), 400

    # Delete all lines and the move itself
    StockMoveLine.query.filter_by(move_id=move.id).delete()
    db.session.delete(move)
    db.session.commit()
    return jsonify({'success': True})


# ─────────────────────────────────────────────
# API: ADD PRODUCT LINE TO OPERATION
# ─────────────────────────────────────────────
@operations_bp.route('/api/operation/<int:move_id>/add-line', methods=['POST'])
def api_add_line(move_id):
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    move = StockMove.query.filter_by(id=move_id, created_by=session['user_id']).first()
    if not move:
        return jsonify({'success': False, 'error': 'Operation not found'}), 404

    if move.status == 'done':
        return jsonify({'success': False, 'error': 'Cannot modify a completed operation'}), 400

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 0))

    if not product_id or quantity <= 0:
        return jsonify({'success': False, 'error': 'Valid product and quantity required'}), 400

    line = StockMoveLine(move_id=move.id, product_id=product_id, quantity=quantity)
    db.session.add(line)
    db.session.commit()

    return jsonify({
        'success': True,
        'line': {
            'id': line.id,
            'product_id': line.product_id,
            'product_name': line.product.name,
            'product_code': line.product.product_code,
            'quantity': line.quantity,
        }
    })


# ─────────────────────────────────────────────
# API: REMOVE PRODUCT LINE FROM OPERATION
# ─────────────────────────────────────────────
@operations_bp.route('/api/operation/<int:move_id>/remove-line', methods=['POST'])
def api_remove_line(move_id):
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    move = StockMove.query.filter_by(id=move_id, created_by=session['user_id']).first()
    if not move:
        return jsonify({'success': False, 'error': 'Operation not found'}), 404

    if move.status == 'done':
        return jsonify({'success': False, 'error': 'Cannot modify a completed operation'}), 400

    data = request.get_json()
    line_id = data.get('line_id')
    line = StockMoveLine.query.filter_by(id=line_id, move_id=move.id).first()
    if not line:
        return jsonify({'success': False, 'error': 'Line not found'}), 404

    db.session.delete(line)
    db.session.commit()
    return jsonify({'success': True})


# ─────────────────────────────────────────────
# API: UPDATE OPERATION FIELDS
# ─────────────────────────────────────────────
@operations_bp.route('/api/operation/<int:move_id>/update', methods=['POST'])
def api_update_operation(move_id):
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401

    move = StockMove.query.filter_by(id=move_id, created_by=session['user_id']).first()
    if not move:
        return jsonify({'success': False, 'error': 'Operation not found'}), 404

    if move.status == 'done':
        return jsonify({'success': False, 'error': 'Cannot modify a completed operation'}), 400

    data = request.get_json()

    if 'contact_id' in data:
        move.contact_id = data['contact_id'] or None
    if 'from_location_id' in data:
        move.from_location_id = data['from_location_id'] or None
    if 'to_location_id' in data:
        move.to_location_id = data['to_location_id'] or None
    if 'schedule_date' in data:
        try:
            move.schedule_date = datetime.strptime(data['schedule_date'], '%Y-%m-%d').date()
        except (ValueError, TypeError):
            pass

    db.session.commit()
    return jsonify({'success': True})


# ─────────────────────────────────────────────
# MOVE HISTORY PAGE (user-scoped)
# ─────────────────────────────────────────────
@operations_bp.route('/move-history')
def move_history_page():
    if not require_login():
        return redirect(url_for('auth.login'))

    uid = session['user_id']
    search = request.args.get('search', '').strip()

    # Fetch all stock moves created by this user
    query = StockMove.query.filter(StockMove.created_by == uid)
    all_moves = query.order_by(StockMove.created_at.desc()).all()

    # Build rows with the fields the template expects
    rows = []
    for m in all_moves:
        total_qty = sum(line.quantity for line in m.lines)
        rows.append({
            'reference': m.reference,
            'schedule_date': m.schedule_date,
            'contact_name': m.contact.name if m.contact else None,
            'from_location': m.from_location.short_code if m.from_location else None,
            'to_location': m.to_location.short_code if m.to_location else None,
            'total_quantity': total_qty,
            'status': m.status,
            'operation_type': m.operation_type,
        })

    # Stats cards
    from sqlalchemy import func as sqlfunc
    total_incoming = (
        db.session.query(sqlfunc.coalesce(sqlfunc.sum(StockMoveLine.quantity), 0))
        .join(StockMove, StockMove.id == StockMoveLine.move_id)
        .filter(StockMove.operation_type == 'receipt', StockMove.status == 'done',
                StockMove.created_by == uid)
        .scalar()
    )
    total_outgoing = (
        db.session.query(sqlfunc.coalesce(sqlfunc.sum(StockMoveLine.quantity), 0))
        .join(StockMove, StockMove.id == StockMoveLine.move_id)
        .filter(StockMove.operation_type == 'delivery', StockMove.status == 'done',
                StockMove.created_by == uid)
        .scalar()
    )
    on_hand = int(total_incoming) - int(total_outgoing)

    return render_template(
        'move_history.html',
        moves=rows,
        total_incoming=int(total_incoming),
        total_outgoing=int(total_outgoing),
        on_hand=on_hand,
        search=search or '',
    )
