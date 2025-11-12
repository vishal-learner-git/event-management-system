# Campus Events and Activities Management System

A comprehensive web-based platform designed specifically for **Sri Manakula Vinayagar Engineering College (SMVEC)** to streamline campus event management, featuring three distinct user portals and modern authentication systems.

![SMVEC Events](https://img.shields.io/badge/SMVEC-Events%20Management-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Firebase](https://img.shields.io/badge/Firebase-Authentication-orange)

## 🏛️ About

This system serves the campus community of Sri Manakula Vinayagar Engineering College by providing a centralized platform for event discovery, creation, management, and participation. The platform facilitates seamless interaction between students, event organizers, and administrators through role-based access control and comprehensive feature sets.

## ✨ Key Features

### 🎯 Multi-Portal Architecture
- **Student Portal**: Event discovery, registration, and participation tracking
- **Organizer Portal**: Event creation, management, and analytics
- **Administrator Portal**: System oversight, user management, and event approval workflows

### 🔐 Advanced Authentication
- **Firebase Google Sign-in**: One-click authentication with Google accounts
- **Manual Registration**: Traditional email/password registration with role selection
- **Enhanced Student Registration**: Includes register number, department selection, and full name
- **Role-Based Access Control**: Secure separation of user permissions

### 📅 Event Management
- **Complete Event Lifecycle**: From creation to completion with approval workflows
- **Rich Event Details**: Venue, timing, categories, capacity, and pricing support
- **Image Upload Support**: Event promotional images with secure handling
- **QR Code Check-in**: Automated attendance tracking system
- **Registration Management**: Capacity limits and automated notifications

### 📊 Analytics & Reporting
- **Event Analytics**: Registration rates, attendance tracking, and performance metrics
- **User Dashboards**: Personalized views for each user type
- **Feedback System**: Event ratings and reviews for continuous improvement
- **Comprehensive Reports**: Administrative insights and statistical analysis

### 🔔 Communication Systems
- **Notification Center**: In-app notifications for important updates
- **Email Integration**: Automated email notifications (configurable)
- **Real-time Updates**: Live status updates for registrations and approvals

## 🛠️ Technology Stack

### Backend Infrastructure
- **Framework**: Flask 2.3.3 (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Firebase Authentication + Custom session management
- **Security**: Werkzeug password hashing with scrypt algorithm
- **File Handling**: Secure image upload with size restrictions

### Frontend Technologies
- **Template Engine**: Jinja2 for server-side rendering
- **UI Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Font Awesome 6.4.0 for comprehensive iconography
- **Charts**: Chart.js for analytics visualization
- **Styling**: Custom CSS with professional blue/white color scheme

### Development & Deployment
- **Server**: Gunicorn WSGI server for production deployment
- **Environment**: Replit-optimized for cloud development
- **Package Management**: Python pip with dependency management
- **Database Migration**: SQLAlchemy database model management

### External Integrations
- **Firebase Services**: Authentication and user management
- **QR Code Generation**: Python qrcode library for attendance
- **Email Services**: SMTP integration for notifications
- **File Storage**: Local file system with secure upload handling

## 🚀 Quick Start

### Automated Setup (Recommended)

1. **Run the automated setup script:**
   ```bash
   python setup.py
   ```

2. **Configure Firebase (if not already done):**
   - Add your Firebase configuration to Replit Secrets:
     - `FIREBASE_API_KEY`
     - `FIREBASE_PROJECT_ID` 
     - `FIREBASE_APP_ID`

3. **Start the application:**
   ```bash
   python main.py
   ```

### Manual Setup

1. **Install Dependencies:**
   ```bash
   pip install flask==2.3.3 werkzeug==2.3.7 gunicorn==21.2.0 psycopg2-binary==2.9.7 flask-sqlalchemy==3.0.5 email-validator==2.0.0 qrcode[pil]==7.4.2
   ```

2. **Set Environment Variables:**
   ```bash
   export DATABASE_URL="your_postgresql_connection_string"
   export FIREBASE_API_KEY="your_firebase_api_key"
   export FIREBASE_PROJECT_ID="your_firebase_project_id"
   export FIREBASE_APP_ID="your_firebase_app_id"
   export SESSION_SECRET="your_secure_session_secret"
   ```

3. **Create Required Directories:**
   ```bash
   mkdir -p static/uploads static/css static/js
   ```

4. **Run the Application:**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

## 👥 User Guide

### Default Administrator Access
- **Email**: `admin@smvec.ac.in`
- **Password**: `admin123`
- **Note**: Change default credentials immediately after first login

### Student Registration Process
1. Visit the homepage and click "Register here"
2. Select "Student" as your role
3. Fill in required information:
   - Full Name
   - Email Address
   - Register Number (e.g., 20CS001)
   - Department Selection
   - Password and Confirmation
4. Complete registration or use Google Sign-in

### Organizer Registration Process
1. Visit the homepage and click "Register as Organizer"
2. Select "Organizer" as your role
3. Provide organization/department information
4. Wait for administrator approval before accessing organizer features

### Event Creation Workflow
1. **Organizer**: Create event with complete details
2. **System**: Event enters "Pending" status
3. **Administrator**: Review and approve/reject event
4. **System**: Approved events become visible to students
5. **Students**: Discover and register for approved events
6. **Organizer**: Track registrations and manage attendance

## 🏗️ System Architecture

### Data Models
- **User**: Stores user information with role-based fields
- **Event**: Complete event information with status tracking
- **Registration**: Links users to events with attendance data
- **Feedback**: Event ratings and comments
- **Notification**: In-app messaging system

### Security Features
- **Password Hashing**: Scrypt algorithm for secure password storage
- **Session Management**: Secure session handling with timeout
- **File Upload Security**: Filename sanitization and size restrictions
- **Access Control**: Role-based route protection
- **Input Validation**: Comprehensive form validation and sanitization

### Database Design
- **Relational Structure**: PostgreSQL with proper foreign key relationships
- **Indexing**: Optimized queries for event discovery and user management
- **Data Integrity**: Constraints and validation at database level
- **Scalability**: Designed to handle growing user base and event volume

## 🔧 Configuration

### Firebase Setup
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Google Authentication in Authentication > Sign-in method
3. Add your domain to Authorized domains list
4. Copy configuration values to environment variables

### Database Configuration
- PostgreSQL database with connection pooling
- Automatic table creation on first run
- Environment-based configuration for different deployment stages

### Email Configuration (Optional)
- SMTP server configuration for notification emails
- Fallback to console logging for development
- Customizable email templates

## 📱 Mobile Responsiveness

The application is built with mobile-first design principles:
- **Bootstrap 5 Grid System**: Responsive layouts for all screen sizes
- **Touch-Friendly Interface**: Optimized for mobile interactions
- **Progressive Enhancement**: Core functionality works without JavaScript
- **Fast Loading**: Optimized assets and minimal dependencies

## 🚀 Deployment Options

### Replit Deployment (Recommended)
- Zero-configuration deployment on Replit platform
- Automatic environment variable management
- Built-in database and file storage
- Instant preview and sharing capabilities

### Traditional Server Deployment
- Gunicorn WSGI server for production
- PostgreSQL database configuration
- Environment variable management
- SSL/TLS configuration for security

### Docker Deployment (Advanced)
- Containerized deployment option
- Multi-stage build for optimization
- Database container orchestration
- Load balancing and scaling support

## 📊 Analytics Features

### Student Analytics
- Personal event registration history
- Attendance tracking and statistics
- Feedback submission history
- Event discovery patterns

### Organizer Analytics
- Event performance metrics
- Registration and attendance rates
- Feedback analysis and ratings
- Participant demographics

### Administrator Analytics
- Platform usage statistics
- Event approval workflows
- User registration trends
- System performance metrics

## 🔒 Security Considerations

### Data Protection
- **Personal Information**: Secure handling of student and organizer data
- **Payment Information**: Secure processing for paid events
- **File Uploads**: Virus scanning and file type validation
- **Database Security**: Encrypted connections and access control

### Privacy Compliance
- **Data Minimization**: Collect only necessary information
- **User Consent**: Clear privacy policy and terms of service
- **Data Retention**: Configurable retention policies
- **Access Rights**: User data access and deletion capabilities

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Implement changes with proper testing
4. Submit pull request with detailed description
5. Code review and integration

### Code Standards
- **Python**: PEP 8 compliance with type hints
- **HTML/CSS**: Semantic markup and accessibility
- **JavaScript**: ES6+ with proper error handling
- **Database**: Normalized design with proper relationships

## 📞 Support & Contact

### Technical Support
- **Development Team**: SMVEC IT Department
- **Documentation**: Comprehensive guides and API references
- **Issue Tracking**: GitHub Issues for bug reports and feature requests

### Institution Contact
- **Sri Manakula Vinayagar Engineering College**
- **Address**: Madagadipet, Puducherry, India
- **Website**: [SMVEC Official](https://smvec.ac.in)

## 📄 License

This project is developed specifically for Sri Manakula Vinayagar Engineering College and is intended for educational and institutional use. Please respect the intellectual property and institutional branding.

## 🙏 Acknowledgments

- **SMVEC Administration**: For vision and support
- **Faculty Advisors**: For guidance and requirements
- **Student Community**: For feedback and testing
- **Open Source Libraries**: For powerful, reliable tools

---

**Sri Manakula Vinayagar Engineering College**  
*Empowering Education Through Technology*

For technical questions or support, please contact the development team or refer to the comprehensive documentation included with this system.