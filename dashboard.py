"""
CoreInventory — Dashboard Routes
Stats are filtered by the logged-in user's operations.
"""

from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from datetime import date
from models import db, StockMove

dashboard_bp = Blueprint('dashboard', __name__)


def require_login():
    return 'user_id' in session


def get_dashboard_stats():
    """Return receipt/delivery counts filtered to the current user's operations."""
    today = date.today()
    uid = session.get('user_id')

    # ── RECEIPTS ──
    # Pending = status 'ready' (ready to receive)
    pending_receipts = StockMove.query.filter(
        StockMove.operation_type == 'receipt',
        StockMove.status == 'ready',
        StockMove.created_by == uid
    ).count()

    # Late = scheduled date < today AND not yet done
    late_receipts = StockMove.query.filter(
        StockMove.operation_type == 'receipt',
        StockMove.status != 'done',
        StockMove.schedule_date < today,
        StockMove.created_by == uid
    ).count()

    # Operations = scheduled date >= today AND not done (upcoming)
    total_receipt_operations = StockMove.query.filter(
        StockMove.operation_type == 'receipt',
        StockMove.status != 'done',
        StockMove.schedule_date >= today,
        StockMove.created_by == uid
    ).count()

    # Waiting = status 'waiting' (waiting for inventory availability)
    waiting_receipts = StockMove.query.filter(
        StockMove.operation_type == 'receipt',
        StockMove.status == 'waiting',
        StockMove.created_by == uid
    ).count()

    # ── DELIVERIES ──
    # Pending = status 'ready' (ready to deliver)
    pending_deliveries = StockMove.query.filter(
        StockMove.operation_type == 'delivery',
        StockMove.status == 'ready',
        StockMove.created_by == uid
    ).count()

    # Late = scheduled date < today AND not yet done
    late_deliveries = StockMove.query.filter(
        StockMove.operation_type == 'delivery',
        StockMove.status != 'done',
        StockMove.schedule_date < today,
        StockMove.created_by == uid
    ).count()

    # Waiting = status 'waiting' (waiting for inventory availability)
    waiting_deliveries = StockMove.query.filter(
        StockMove.operation_type == 'delivery',
        StockMove.status == 'waiting',
        StockMove.created_by == uid
    ).count()

    # Operations = scheduled date >= today AND not done (upcoming)
    total_delivery_operations = StockMove.query.filter(
        StockMove.operation_type == 'delivery',
        StockMove.status != 'done',
        StockMove.schedule_date >= today,
        StockMove.created_by == uid
    ).count()

    return {
        'pending_receipts': pending_receipts,
        'late_receipts': late_receipts,
        'total_receipt_operations': total_receipt_operations,
        'waiting_receipts': waiting_receipts,
        'pending_deliveries': pending_deliveries,
        'late_deliveries': late_deliveries,
        'waiting_deliveries': waiting_deliveries,
        'total_delivery_operations': total_delivery_operations,
    }


@dashboard_bp.route('/dashboard')
def index():
    if not require_login():
        return redirect(url_for('auth.login'))

    stats = get_dashboard_stats()
    return render_template('dashboard.html', **stats)


@dashboard_bp.route('/api/dashboard-stats')
def api_stats():
    if not require_login():
        return jsonify({'error': 'not logged in'}), 401
    return jsonify(get_dashboard_stats())