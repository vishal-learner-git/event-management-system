from functools import wraps
from flask import session, redirect, url_for, flash
from models import data_store, Notification
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import qrcode
import io
import base64

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page', 'error')
                if role == 'student':
                    return redirect(url_for('auth.student_login'))
                elif role == 'organizer':
                    return redirect(url_for('auth.organizer_login'))
                elif role == 'admin':
                    return redirect(url_for('auth.admin_login'))
                else:
                    return redirect(url_for('index'))
            
            if role and session.get('user_role') != role:
                flash('Access denied', 'error')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def send_notification(user_id, title, message, notification_type='info'):
    """Send in-app notification to user"""
    notification = Notification(user_id, title, message, notification_type)
    data_store.notifications[notification.id] = {
        'id': notification.id,
        'user_id': notification.user_id,
        'title': notification.title,
        'message': notification.message,
        'type': notification.type,
        'read': notification.read,
        'created_at': notification.created_at
    }
    
    # Optional: Send email notification
    user = data_store.users.get(user_id)
    if user:
        send_email(user['email'], title, message)

def send_email(to_email, subject, message):
    """Send email notification (mock implementation for MVP)"""
    # This is a mock implementation
    # In production, configure with actual SMTP settings
    try:
        # Mock email sending - just log it
        print(f"EMAIL SENT TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print(f"MESSAGE: {message}")
        print("-" * 50)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def generate_qr_code(text):
    """Generate QR code for event check-in"""
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for embedding in HTML
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
    except ImportError:
        # Fallback if qrcode library is not available
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg', 'gif'}):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def format_datetime(dt):
    """Format datetime for display"""
    return dt.strftime('%B %d, %Y at %I:%M %p')

def get_user_notifications(user_id, limit=10):
    """Get recent notifications for user"""
    user_notifications = []
    for notif_id, notif in data_store.notifications.items():
        if notif['user_id'] == user_id:
            user_notifications.append(notif)
    
    # Sort by creation date (newest first)
    user_notifications.sort(key=lambda x: x['created_at'], reverse=True)
    
    return user_notifications[:limit]

def mark_notification_read(notification_id):
    """Mark notification as read"""
    notification = data_store.notifications.get(notification_id)
    if notification:
        notification['read'] = True
        return True
    return False
