# crown-wave

```
gunicorn -w 4 -b 127.0.0.1:8000 migration.app:app


```
Crown-wave
it is an investement website
   frontend-html
                    jinja-templating

Backend
User Requirements
The backend must fulfill the following user requirements:
    1. Admin Users:
        ◦ Ability to log in securely.
        ◦ Manage website content, including adding, editing, or removing information.
        ◦ View analytics and reports on website usage.
    2. End Users (Visitors):
        ◦ Access website content efficiently.
        ◦ Contact the CEO or Crown Wave team via forms.
        ◦ Receive responses to inquiries within a specified timeframe.

3. User Stories
Admin User Stories:
    • As an admin, I want to log in securely so that I can manage the website content.
    • As an admin, I want to manage inquiries so that I can respond promptly to user questions.
    • As an admin, I want to generate reports so that I can analyze website traffic.
End User Stories:
    • As a user, I want to access information about the CEO so that I can learn more about the leadership.
    • As a user, I want to submit a contact form so that I can ask questions or provide feedback.
    • As a user, I want a seamless browsing experience so that I can navigate the website efficiently.

4. Backend Features
Core Features:
    1. User Authentication & Authorization:
        ◦ Secure user login/logout functionality.
        ◦ Role-based access control (admin vs. end-users).
    2. Content Management System (CMS):
        ◦ APIs for adding, updating, and deleting website content (e.g., CEO bio, contact info).
    3. Contact Form Handling:
        ◦ Endpoint to handle form submissions.
        ◦ Integration with an email service for automatic responses.
        ◦ Store form data in a database for future reference.
    4. Analytics and Reporting:
        ◦ APIs to track and retrieve website usage statistics.
        ◦ Admin dashboard for viewing reports.
    5. API Endpoints for Frontend:
        ◦ RESTful APIs to serve website content dynamically.
        ◦ Support for JSON responses for frontend integration.

5. Technical Stack
    1. Framework: Flask (Python).
    2. Database: SQLite (for development) and PostgreSQL (for production).
    3. ORM: SQLAlchemy for database management.
    4. Authentication: Flask-Security or Flask-JWT-Extended for secure user authentication.
    5. Form Handling: Flask-WTF for form validations.
    6. Email Service: Flask-Mail for sending email notifications.
    7. Hosting: Deployment on platforms like AWS, Heroku, or DigitalOcean.

6. Database Schema
Tables:
    1. Users:
        ◦ id: Integer, Primary Key.
        ◦ username: String, Unique.
        ◦ password_hash: String.
        ◦ role: String (e.g., "admin" or "user").
    2. Content:
        ◦ id: Integer, Primary Key.
        ◦ title: String.
        ◦ body: Text.
        ◦ created_at: Timestamp.
    3. ContactFormSubmissions:
        ◦ id: Integer, Primary Key.
        ◦ name: String.
        ◦ email: String.
        ◦ message: Text.
        ◦ submitted_at: Timestamp.
    4. Analytics:
        ◦ id: Integer, Primary Key.
        ◦ page: String.
        ◦ visits: Integer.

7. API Endpoints
Authentication:
    • POST /auth/login: User login.
    • POST /auth/logout: User logout.
Content Management:
    • GET /api/content: Retrieve website content.
    • POST /api/content: Add new content (admin only).
    • PUT /api/content/<id>: Update content (admin only).
    • DELETE /api/content/<id>: Delete content (admin only).
Contact Form:
    • POST /api/contact: Submit a contact form.
Analytics:
    • GET /api/analytics: Retrieve website analytics (admin only).

8. Features for Future Enhancements
    1. Add real-time chat support for users to contact the CEO or team.
    2. Implement AI-driven analytics for better insights into user behavior.
    3. Introduce multi-language support for global users.
    4. Add notifications for admins about new contact form submissions.

9. Development Workflow
    1. Setup Flask Environment:
        ◦ Create a virtual environment and install dependencies.
        ◦ Initialize the Flask app and configure settings.
    2. Database Design:
        ◦ Define models using SQLAlchemy.
        ◦ Migrate schemas to the database.
    3. API Development:
        ◦ Implement routes for authentication, content management, and contact forms.
        ◦ Test all endpoints using Postman.
    4. Security Implementation:
        ◦ Secure sensitive endpoints with authentication and authorization.
        ◦ Protect user data with password hashing and SSL.
    5. Testing:
        ◦ Write unit and integration tests for all features.
        ◦ Ensure the API is robust and free from vulnerabilities.
          
    6. Deployment:
        ◦ Deploy the backend to a production server with proper configurations.
7.   Requirements:
alembic==1.13.3
backoff==2.2.1
bcrypt==4.2.0
blinker==1.8.2
branca==0.7.2
certifi==2024.6.2
charset-normalizer==3.3.2
click==8.1.7
decorator==5.1.1
distlib==0.3.8
filelock==3.15.4
Flask==3.0.3
Flask-Bcrypt==1.0.1
Flask-JWT-Extended==4.6.0
Flask-Login==0.6.3
Flask-Mail==0.10.0
Flask-Migrate==4.0.7
Flask-Scrypt==0.1.3.6
Flask-SQLAlchemy==3.1.1
folium==0.17.0
future==1.0.0
geocoder==1.38.1
geographiclib==2.0
geopy==2.4.1
greenlet==3.1.1
gunicorn==23.0.0
h11==0.14.0
idna==3.7
importlib_metadata==8.4.0
importlib_resources==6.4.5
itsdangerous==2.2.0
Jinja2==3.1.4
Mako==1.3.5
MarkupSafe==2.1.5
numpy==1.24.4
packaging==24.1
pipenv==2024.0.1
platformdirs==4.2.2
psycopg2==2.9.10
PyJWT==2.9.0
python-dotenv==1.0.1
ratelim==0.1.6
requests==2.32.3
scrypt==0.8.27
six==1.16.0
SQLAlchemy==2.0.35
typing_extensions==4.12.2
urllib3==2.2.2
uvicorn==0.32.0
virtualenv==20.26.3
Werkzeug==3.0.4
xyzservices==2024.6.0
zipp==3.20.1



n