from datetime import datetime
import uuid
import json
import os

def convert_datetime_strings(obj):
    """Convert datetime strings back to datetime objects"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key.endswith('_at') or key.endswith('_date'):
                if isinstance(value, str):
                    try:
                        obj[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except (ValueError, AttributeError):
                        pass
            elif isinstance(value, (dict, list)):
                convert_datetime_strings(value)
    elif isinstance(obj, list):
        for item in obj:
            convert_datetime_strings(item)
    return obj

# Persistent storage using JSON files
class DataStore:
    def __init__(self, data_file='data/datastore.json'):
        # Ensure the data file path is relative to the CampusEventManager directory
        import os
        if not os.path.isabs(data_file):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_file = os.path.join(current_dir, data_file)
        else:
            self.data_file = data_file
        self.users = {}
        self.events = {}
        self.registrations = {}
        self.feedback = {}
        self.notifications = {}

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        # Load existing data or initialize with default admin
        self.load_data()

        # Ensure admin user exists
        if 'admin' not in self.users:
            self.users['admin'] = {
                'id': 'admin',
                'username': 'admin',
                'email': 'admin@smvec.ac.in',
                'password_hash': 'scrypt:32768:8:1$m7CjGjKoQF5pjS2M$8c0ae6d9c0ef1e5c3b9f8d6e7a4b5c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0',
                'role': 'admin',
                'created_at': datetime.now().isoformat(),
                'is_active': True,
                'full_name': 'Administrator',
                'register_number': None,
                'department': None
            }
            self.save_data()

    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.users = convert_datetime_strings(data.get('users', {}))
                    self.events = convert_datetime_strings(data.get('events', {}))
                    self.registrations = convert_datetime_strings(data.get('registrations', {}))
                    self.notifications = convert_datetime_strings(data.get('notifications', {}))
                    self.feedback = convert_datetime_strings(data.get('feedback', {}))
            except (json.JSONDecodeError, FileNotFoundError):
                self.initialize_default_data()
        else:
            self.initialize_default_data()

    def initialize_default_data(self):
        """Initialize with default data if file not found or corrupted"""
        print("Initializing default data.")
        self.users = {
            'admin': {
                'id': 'admin',
                'username': 'admin',
                'email': 'admin@smvec.ac.in',
                'password_hash': 'scrypt:32768:8:1$m7CjGjKoQF5pjS2M$8c0ae6d9c0ef1e5c3b9f8d6e7a4b5c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0',
                'role': 'admin',
                'created_at': datetime.now().isoformat(),
                'is_active': True,
                'full_name': 'Administrator',
                'register_number': None,
                'department': None
            }
        }
        self.events = {}
        self.registrations = {}
        self.feedback = {}
        self.notifications = {}
        self.save_data()


    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                'users': self.users,
                'events': self.events,
                'registrations': self.registrations,
                'feedback': self.feedback,
                'notifications': self.notifications
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f"Data saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_user(self, user_id, user_data):
        """Add a user and save data"""
        self.users[user_id] = user_data
        self.save_data()

    def add_event(self, event_id, event_data):
        """Add an event and save data"""
        self.events[event_id] = event_data
        self.save_data()

    def add_registration(self, reg_id, reg_data):
        """Add a registration and save data"""
        self.registrations[reg_id] = reg_data
        self.save_data()

    def add_feedback(self, feedback_id, feedback_data):
        """Add feedback and save data"""
        self.feedback[feedback_id] = feedback_data
        self.save_data()

    def add_notification(self, notification_id, notification_data):
        """Add notification and save data"""
        self.notifications[notification_id] = notification_data
        self.save_data()

    def update_user(self, user_id, user_data):
        """Update a user and save data"""
        self.users[user_id] = user_data
        self.save_data()

    def update_event(self, event_id, event_data):
        """Update an event and save data"""
        self.events[event_id] = event_data
        self.save_data()

    def delete_user(self, user_id):
        """Delete a user and save data"""
        if user_id in self.users:
            del self.users[user_id]
            self.save_data()

    def delete_event(self, event_id):
        """Delete an event and save data"""
        if event_id in self.events:
            del self.events[event_id]
            self.save_data()

data_store = DataStore()

class User:
    def __init__(self, username, email, password_hash, role='student', register_number=None, department=None, full_name=None):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = datetime.now()
        self.is_active = True
        # Additional fields for students
        self.register_number = register_number
        self.department = department
        self.full_name = full_name or username

class Event:
    def __init__(self, title, description, organizer_id, venue, start_date, end_date, category, max_attendees=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.organizer_id = organizer_id
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.category = category
        self.max_attendees = max_attendees
        self.current_attendees = 0
        self.status = 'pending'  # pending, approved, rejected
        self.created_at = datetime.now()
        self.image_path = ""
        self.is_paid = False
        self.price = 0.0

class Registration:
    def __init__(self, user_id, event_id):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.event_id = event_id
        self.registered_at = datetime.now()
        self.attended = False
        self.qr_code = str(uuid.uuid4())

class Feedback:
    def __init__(self, user_id, event_id, rating, comment):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.event_id = event_id
        self.rating = rating
        self.comment = comment
        self.created_at = datetime.now()

class Notification:
    def __init__(self, user_id, title, message, notification_type='info'):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = notification_type
        self.read = False
        self.created_at = datetime.now()