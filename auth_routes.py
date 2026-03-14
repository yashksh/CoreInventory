"""
CoreInventory — Authentication Routes
Login, Signup (with validation), Logout, Forgot Password (OTP via email), Reset Password.
"""

import re
import random
from datetime import datetime, timedelta

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, current_app
)
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, PasswordResetToken

auth_bp = Blueprint('auth', __name__)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def validate_password(password):
    """
    Password must be:
    - At least 8 characters
    - Contain at least one uppercase letter
    - Contain at least one lowercase letter
    - Contain at least one special character
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        return False, "Password must contain at least one special character"
    return True, None


def validate_login_id(login_id):
    """Login ID must be 6-12 characters."""
    if len(login_id) < 6:
        return False, "Login ID must be at least 6 characters"
    if len(login_id) > 12:
        return False, "Login ID must not exceed 12 characters"
    return True, None


def generate_otp():
    """Generate a random 6-digit OTP."""
    return str(random.randint(100000, 999999))


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        login_id = request.form.get('login_id', '').strip()
        password = request.form.get('password', '')

        if not login_id or not password:
            error = "Please enter Login ID and Password"
            return render_template('login.html', error=error)

        user = User.query.filter_by(login_id=login_id).first()

        if user is None or not check_password_hash(user.password_hash, password):
            error = "Invalid Login ID or Password"
            return render_template('login.html', error=error)

        # ── Create session ──
        session.clear()
        session['user_id']  = user.id
        session['login_id'] = user.login_id
        session['email']    = user.email
        session.permanent   = True

        return redirect(url_for('dashboard.index'))

    return render_template('login.html', error=error)


# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# ─────────────────────────────────────────────
# SIGNUP  (with validation)
# ─────────────────────────────────────────────
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        login_id = request.form.get('login_id', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        # All fields required
        if not login_id or not email or not password:
            error = "All fields are required"
        else:
            # Validate login ID length (6-12 chars)
            valid_id, id_err = validate_login_id(login_id)
            if not valid_id:
                error = id_err

            # Validate password strength
            elif password != confirm:
                error = "Passwords do not match"
            else:
                valid_pw, pw_err = validate_password(password)
                if not valid_pw:
                    error = pw_err

            # Check uniqueness
            if not error:
                if User.query.filter_by(login_id=login_id).first():
                    error = "Login ID already exists"
                elif User.query.filter_by(email=email).first():
                    error = "Email already registered"

        if error:
            return render_template('signup.html', error=error)

        new_user = User(
            login_id=login_id,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('signup.html', error=None)


# ─────────────────────────────────────────────
# FORGOT PASSWORD  (send OTP to email)
# ─────────────────────────────────────────────
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    error = None
    success = None

    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        if not email:
            error = "Please enter your email address"
        else:
            user = User.query.filter_by(email=email).first()

            if user is None:
                error = "No account found with that email"
            else:
                # Invalidate any previous unused tokens for this user
                PasswordResetToken.query.filter_by(
                    user_id=user.id, used=False
                ).update({'used': True})
                db.session.commit()

                # Generate new OTP
                otp = generate_otp()
                token = PasswordResetToken(
                    user_id=user.id,
                    otp=otp,
                    expires_at=datetime.utcnow() + timedelta(minutes=10)
                )
                db.session.add(token)
                db.session.commit()

                # Send email
                try:
                    from flask_mail import Message as MailMessage
                    mail = current_app.extensions['mail']
                    msg = MailMessage(
                        subject="CoreInventory — Password Reset OTP",
                        recipients=[email],
                    )
                    msg.html = f"""
                    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;
                                padding: 32px; background: #f8fafc; border-radius: 12px;">
                        <h2 style="color: #4f46e5; margin-bottom: 8px;">CoreInventory</h2>
                        <p style="color: #475569;">Your password reset OTP is:</p>
                        <div style="font-size: 32px; font-weight: 700; letter-spacing: 8px;
                                    color: #1e293b; background: #ffffff; border: 2px solid #e2e8f0;
                                    border-radius: 8px; padding: 16px; text-align: center; margin: 16px 0;">
                            {otp}
                        </div>
                        <p style="color: #64748b; font-size: 14px;">
                            This OTP is valid for <strong>10 minutes</strong>. Do not share it with anyone.
                        </p>
                    </div>
                    """
                    mail.send(msg)
                    # Store email in session for the reset step
                    session['reset_email'] = email
                    flash("OTP has been sent to your email. Check your inbox.", "success")
                    return redirect(url_for('auth.reset_password'))

                except Exception as e:
                    error = f"Failed to send email. Please check email configuration. ({e})"

    return render_template('forgot_password.html', error=error, success=success)


# ─────────────────────────────────────────────
# RESET PASSWORD  (verify OTP + set new password)
# ─────────────────────────────────────────────
@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    error = None
    email = session.get('reset_email', '')

    if not email:
        flash("Please request an OTP first.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        otp          = request.form.get('otp', '').strip()
        new_password = request.form.get('password', '')
        confirm      = request.form.get('confirm_password', '')

        if not otp or not new_password or not confirm:
            error = "All fields are required"
        elif new_password != confirm:
            error = "Passwords do not match"
        else:
            # Validate password strength
            valid_pw, pw_err = validate_password(new_password)
            if not valid_pw:
                error = pw_err

        if not error:
            user = User.query.filter_by(email=email).first()
            if not user:
                error = "User not found"
            else:
                # Find the latest unused token for this user
                token = PasswordResetToken.query.filter_by(
                    user_id=user.id,
                    otp=otp,
                    used=False
                ).order_by(PasswordResetToken.created_at.desc()).first()

                if token is None:
                    error = "Invalid OTP. Please try again."
                elif token.is_expired():
                    error = "OTP has expired. Please request a new one."
                else:
                    # OTP is valid! Update password
                    user.password_hash = generate_password_hash(new_password)
                    token.used = True
                    db.session.commit()

                    session.pop('reset_email', None)
                    flash("Password reset successful! Please login with your new password.", "success")
                    return redirect(url_for('auth.login'))

    return render_template('reset_password.html', error=error, email=email)