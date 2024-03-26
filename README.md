Scholarship Hours Tracking Project
Description
This project is a web application designed to help students track their scholarship hours. It allows students to register for events, log their hours, and provides administrators with tools to manage events and track student participation.

Features
User registration and authentication
Event registration for students
Event management for administrators
Logging of scholarship hours
User profile management
Responsive design for mobile and desktop
Technologies Used
Frontend: HTML, CSS, JavaScript, Bootstrap
Backend: Python, Flask
Database: MySQL
Other Tools: Flask-SQLAlchemy, Flask-Login, Jinja2 templates
Setup
Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/scholarship-hours-project.git
Install dependencies:
Copy code
pip install -r requirements.txt
Create a MySQL database and update the database configuration in config.py.
Initialize the database:
csharp
Copy code
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
Run the application:
Copy code
python app.py