# replit.md

## Overview

The Campus Events and Activities Management System for Sri Manakula Vinayagar Engineering College (SMVEC) is a comprehensive web platform built with Flask that facilitates event management across the campus community. The system serves three distinct user types: students who can discover and register for events, organizers who can create and manage events, and administrators who oversee the entire platform with approval workflows and analytics.

The platform provides a centralized hub for campus event lifecycle management, from creation and approval to registration, attendance tracking, and feedback collection. Key features include role-based authentication, event discovery with filtering capabilities, automated notifications, QR code-based attendance management, and comprehensive analytics dashboards.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The system uses a server-side rendered architecture with Flask templates and Jinja2 templating engine. The frontend is built with responsive Bootstrap 5 components, ensuring mobile-first design principles. JavaScript enhancements provide interactive features like form validation, dynamic filtering, and chart visualizations using Chart.js for analytics dashboards.

The template structure follows a modular approach with a base template that provides common navigation and styling, while role-specific templates extend this base for students, organizers, and administrators. Static assets are organized with separate CSS and JavaScript files for maintainability.

### Backend Architecture
The Flask application follows a blueprint-based modular architecture, separating concerns across authentication (`auth.py`), student portal (`student/routes.py`), organizer portal (`organizer/routes.py`), and admin portal (`admin/routes.py`). The main application (`app.py`) serves as the entry point, registering blueprints with appropriate URL prefixes.

Session-based authentication manages user state across requests, with role-based access control implemented through decorators in `utils.py`. The system includes middleware for proxy handling and file upload management with size limits and secure filename handling.

### Data Storage Solutions
Currently implements an in-memory data store pattern (`models.py`) using Python dictionaries for rapid prototyping and development. The `DataStore` class manages users, events, registrations, feedback, and notifications in memory, with model classes (User, Event, Registration) providing structured data representation.

This approach allows for quick development iteration but is designed to be easily replaceable with a proper database backend like PostgreSQL using an ORM such as SQLAlchemy or Drizzle in future iterations.

### Authentication and Authorization
The system implements a three-tier authentication model supporting students, organizers, and administrators. Password hashing uses Werkzeug's security utilities with scrypt algorithm for secure password storage. Role-based access control is enforced through decorators that check both authentication status and user roles before allowing access to protected routes.

Session management handles user state persistence across requests, with automatic logout functionality and role-specific dashboard redirections. The authentication system includes registration workflows for students and organizers, with administrative approval required for organizer accounts.

### Event Management System
Events follow a complete lifecycle from creation to completion. Organizers can create events with detailed information including venue, timing, categories, and optional pricing. The system supports file uploads for event images with secure filename handling and size restrictions.

An approval workflow requires administrative review before events become visible to students. Event status tracking (pending, approved, rejected) provides clear visibility into the approval process. Registration management includes capacity limits, attendance tracking via QR codes, and automated notification systems.

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5.3.0**: Responsive CSS framework for UI components and grid system
- **Font Awesome 6.4.0**: Icon library for consistent iconography across the platform
- **Chart.js**: JavaScript charting library for analytics dashboards and data visualization

### Backend Dependencies
- **Flask**: Core web framework providing routing, request handling, and template rendering
- **Werkzeug**: WSGI utilities including security functions for password hashing and file handling
- **Jinja2**: Template engine integrated with Flask for server-side rendering

### Development and Deployment
- **ProxyFix Middleware**: Werkzeug middleware for handling proxy headers in deployment environments
- **File Upload System**: Built-in Flask file handling with security measures for event image uploads

### Notification System
The platform includes infrastructure for email notifications using SMTP, though specific email service providers can be configured based on deployment requirements. QR code generation capabilities are built-in for attendance management features.

### Future Integration Readiness
The architecture is designed to accommodate future integrations including Google Calendar API for calendar synchronization, payment gateway integration for paid events, and database backends like PostgreSQL for production deployment. The modular structure allows for easy addition of these services without major architectural changes.