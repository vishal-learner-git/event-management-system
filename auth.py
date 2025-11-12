from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import data_store, User
import logging
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find user by email
        user = None
        for uid, u in data_store.users.items():
            if u['email'] == email and u['role'] == 'student':
                user = u
                break

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            session['username'] = user['username']
            flash('Welcome back!', 'success')
            return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth/student_login.html',
                         firebase_api_key=os.environ.get('FIREBASE_API_KEY'),
                         firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID'),
                         firebase_app_id=os.environ.get('FIREBASE_APP_ID'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html', 
                                 firebase_api_key=os.environ.get('FIREBASE_API_KEY'),
                                 firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID'),
                                 firebase_app_id=os.environ.get('FIREBASE_APP_ID'))

        if role not in ['student', 'organizer', 'admin']:
            flash('Invalid role selected', 'error')
            return render_template('auth/register.html',
                                 firebase_api_key=os.environ.get('FIREBASE_API_KEY'),
                                 firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID'),
                                 firebase_app_id=os.environ.get('FIREBASE_APP_ID'))

        # Check if email already exists
        for uid, user in data_store.users.items():
            if user['email'] == email:
                flash('Email already registered', 'error')
                return render_template('auth/register.html',
                                     firebase_api_key=os.environ.get('FIREBASE_API_KEY'),
                                     firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID'),
                                     firebase_app_id=os.environ.get('FIREBASE_APP_ID'))

        # Get role-specific fields
        register_number = None
        department = None
        organization = None

        if role == 'student':
            register_number = request.form.get('register_number')
            department = request.form.get('department')
            if not register_number or not department:
                flash('Register number and department are required for students', 'error')
                return render_template('auth/register.html',
                                     firebase_api_key=os.environ.get('FIREBASE_API_KEY'),
                                     firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID'),
                                     firebase_app_id=os.environ.get('FIREBASE_APP_ID'))
        elif role == 'organizer':
            organization = request.form.get('organization')

        # Create new user
        user = User(full_name, email, generate_password_hash(password), role, register_number, department, full_name)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'role': user.role,
            'created_at': user.created_at,
            'is_active': user.is_active,
            'full_name': user.full_name,
            'register_number': user.register_number,
            'department': user.department
        }

        if role == 'organizer':
            user_data['organization'] = organization

        data_store.add_user(user.id, user_data)

        flash(f'{role.title()} registration successful! Please login.', 'success')
        return redirect(url_for('index'))

    return render_template('auth/register.html',
                         firebase_api_key=os.environ.get('FIREBASE_API_KEY'),
                         firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID'),
                         firebase_app_id=os.environ.get('FIREBASE_APP_ID'))

@auth_bp.route('/organizer/login', methods=['GET', 'POST'])
def organizer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find user by email
        user = None
        for uid, u in data_store.users.items():
            if u['email'] == email and u['role'] == 'organizer':
                user = u
                break

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            session['username'] = user['username']
            flash('Welcome back!', 'success')
            return redirect(url_for('organizer.dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth/organizer_login.html',
                         firebase_api_key=os.environ.get('FIREBASE_API_KEY'),
                         firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID'),
                         firebase_app_id=os.environ.get('FIREBASE_APP_ID'))

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find user by email
        user = None
        for uid, u in data_store.users.items():
            if u['email'] == email and u['role'] == 'admin':
                user = u
                break

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            session['username'] = user['username']
            flash('Welcome back, Administrator!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth/admin_login.html',
                         firebase_api_key=os.environ.get('FIREBASE_API_KEY'),
                         firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID'),
                         firebase_app_id=os.environ.get('FIREBASE_APP_ID'))

@auth_bp.route('/admin/register', methods=['POST'])
def admin_register():
    admin_code = request.form['admin_code']
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Validate admin code
    if admin_code != 'Admin@2024':
        flash('Invalid admin code. Access denied.', 'error')
        return redirect(url_for('auth.admin_login'))

    # Validation
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('auth.admin_login'))

    # Check if email already exists
    for uid, user in data_store.users.items():
        if user['email'] == email:
            flash('Email already registered', 'error')
            return redirect(url_for('auth.admin_login'))

    # Create new admin user
    user = User(full_name, email, generate_password_hash(password), 'admin', None, None, full_name)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password_hash': user.password_hash,
        'role': user.role,
        'created_at': user.created_at,
        'is_active': user.is_active,
        'full_name': user.full_name,
        'register_number': user.register_number,
        'department': user.department
    }

    data_store.add_user(user.id, user_data)

    flash('Admin registration successful! Please login with your new credentials.', 'success')
    return redirect(url_for('auth.admin_login'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))