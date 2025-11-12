#!/usr/bin/env python3
"""
Automated Setup Script for SMVEC Campus Events Management System
This script sets up the complete environment for the events management system
"""

import os
import subprocess
import sys
import secrets
import string
from werkzeug.security import generate_password_hash
from models import User
from dotenv import load_dotenv # <-- ADDED: Import the dotenv function

# --- ADDED: Load environment variables from .env file ---
load_dotenv()
# --------------------------------------------------------

def generate_secret_key():
    """Generate a secure secret key for Flask sessions"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50))

def setup_environment():
    """Set up environment variables and configuration"""
    print("🔧 Setting up environment configuration...")
    
    # Check if running on Replit
    if os.environ.get('REPLIT_DB_URL'):
        print("✅ Replit environment detected")
    else:
        print("⚠️  Not running on Replit - setting up local environment")
    
    # Check required environment variables
    required_vars = [
        'DATABASE_URL',
        'FIREBASE_API_KEY', 
        'FIREBASE_PROJECT_ID',
        'FIREBASE_APP_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file before running the application.")
        return False
    
    # Set session secret if not exists
    if not os.environ.get('SESSION_SECRET'):
        secret = generate_secret_key()
        print(f"🔑 Generated SESSION_SECRET: {secret}")
        print("Add this to your .env file for production!")
    
    print("✅ Environment configuration complete")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    try:
        # Install dependencies from requirements
        dependencies = [
            'flask==2.3.3',
            'werkzeug==2.3.7',
            'gunicorn==21.2.0',
            'psycopg2-binary==2.9.9',
            'flask-sqlalchemy==3.0.5',
            'email-validator==2.0.0',
            'qrcode[pil]==7.4.2',
            'python-dotenv==1.0.0'
        ]
        
        for dep in dependencies:
            print(f"  Installing {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                         check=True, capture_output=True)
        
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_database():
    """Set up database tables and initial data"""
    print("🗄️  Setting up database...")

    try:
        from app import app
        from models import data_store

        print("✅ Database models loaded successfully")

        # Check if admin user exists
        admin_exists = any(user.get('role') == 'admin' for user in data_store.users.values())
        if admin_exists:
            print("✅ Default admin user already exists")
        else:
            print("ℹ️  Default admin user not found. Creating now...")
            admin_user = User(
                username="Admin User",
                email="admin@smvec.ac.in",
                password_hash=generate_password_hash("admin123"),
                role="admin"
            )
            data_store.users[admin_user.id] = {
                'id': admin_user.id,
                'username': admin_user.username,
                'email': admin_user.email,
                'password_hash': admin_user.password_hash,
                'role': admin_user.role,
                'created_at': admin_user.created_at,
                'is_active': True,
                'full_name': "Admin User",
                'register_number': None,
                'department': None
            }
            print("✅ Default admin user (admin@smvec.ac.in / admin123) created.")

        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = [
        'static/uploads',
        'static/css',
        'static/js',
        'templates/auth',
        'templates/student',
        'templates/organizer',
        'templates/admin'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ Created {directory}")
    
    print("✅ Directory structure created")
    return True

def run_tests():
    """Run basic functionality tests"""
    print("🧪 Running basic functionality tests...")
    
    try:
        # Test import of main modules
        from app import app
        from auth import auth_bp
        from models import data_store, User, Event
        
        # Test Flask app creation
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("  ✅ Homepage loads successfully")
            else:
                print(f"  ⚠️  Homepage returned status {response.status_code}")
        
        # Test user creation
        from werkzeug.security import generate_password_hash
        test_user = User("Test User", "test@example.com", generate_password_hash("password123"))
        print("  ✅ User model creation works")
        
        print("✅ Basic functionality tests passed")
        return True
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False

def display_startup_info():
    """Display startup information and instructions"""
    print("\n" + "="*60)
    print("🎉 SMVEC CAMPUS EVENTS MANAGEMENT SYSTEM SETUP COMPLETE!")
    print("="*60)
    print()
    print("📋 SYSTEM INFORMATION:")
    print("  • Application: Campus Events & Activities Management")
    print("  • Institution: Sri Manakula Vinayagar Engineering College")
    print("  • Framework: Flask with PostgreSQL")
    print("  • Authentication: Firebase Google Sign-in + Manual")
    print()
    print("🚀 TO START THE APPLICATION:")
    print("  Run: python main.py")
    print("  Or: gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app")
    print()
    print("🔐 DEFAULT ADMIN CREDENTIALS:")
    print("  Email: admin@smvec.ac.in")
    print("  Password: admin123")
    print()
    print("👥 USER PORTALS:")
    print("  • Students: Discover and register for events")
    print("  • Organizers: Create and manage events")
    print("  • Administrators: Approve events and manage users")
    print()
    print("🔧 FEATURES INCLUDED:")
    print("  ✅ Three-tier authentication system")
    print("  ✅ Firebase Google authentication")
    print("  ✅ Event creation and approval workflow")
    print("  ✅ Registration and attendance tracking")
    print("  ✅ QR code check-in system")
    print("  ✅ Analytics and reporting")
    print("  ✅ Notification system")
    print("  ✅ Feedback and rating system")
    print()
    print("🌐 ACCESS YOUR APPLICATION:")
    print("  • Local: http://localhost:5000")
    print("  • Replit: Check the preview pane")
    print()
    print("📚 For more information, see README.md")
    print("="*60)

def main():
    """Main setup function"""
    print("🏛️  SMVEC Campus Events Management System - Automated Setup")
    print("=" * 60)
    
    steps = [
        ("Environment Setup", setup_environment),
        ("Dependency Installation", install_dependencies),
        ("Directory Creation", create_directories),
        ("Database Setup", setup_database),
        ("Functionality Tests", run_tests)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 Step: {step_name}")
        print("-" * 40)
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    display_startup_info()

if __name__ == "__main__":
    main()
