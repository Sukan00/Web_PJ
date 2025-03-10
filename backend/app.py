import psycopg2
import os
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

''' Database connection details Class '''
class Database:
    DB_CONFIG = {
        "host": os.environ.get('DB_HOST', 'localhost'),
        "dbname": os.environ.get('DB_NAME', 'DB'),
        "user": os.environ.get('DB_USER', 'postgres'),
        "password": os.environ.get('DB_PASSWORD', '1234'),
        "port": 5432
    }

    @classmethod
    def connect_db(cls):
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**cls.DB_CONFIG)
        return conn
    
    @classmethod
    def execute_query(cls, query, params=None, fetch=False):
        conn = cls.connect_db()
        cur = conn.cursor()
        try:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            conn.commit()
        finally:
            cur.close()
            conn.close()
    
''' Class User
              cls = accessing the User class by itself  '''
class User:
    def __init__(self, user_id, email, role):
        self.user_id = user_id
        self.email = email
        self.role = role

    # Check if the user with the given email and password exists in the database 
    @classmethod
    def authenticate(cls, email, password):
        conn = Database.connect_db()
        cur = conn.cursor()

        cur.execute('SELECT user_id, email, role FROM "user" WHERE email = %s AND password = %s', (email, password))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return cls(user_id=user[0], email=user[1], role=user[2])
        return None
    
    # Query detail user
    @classmethod
    def get_user(cls, email):
        conn = cls.connect()
        cur = conn.cursor()

        cur.execute('SELECT email, role FROM "user" WHERE email = %s', (email,))
        user_detail = cur.fetchone()

        cur.close()
        conn.close()

        if user_detail:
            return cls(user_id=user_detail[0], email=user_detail[1], role=user_detail[2])
        return None

''' Class Report '''
class Report:
    def __init__(self, title, intro, year, category, path, org=None, type_org=None, position=None):
        self.title = title
        self.intro = intro
        self.year = year
        self.category = category
        self.path = path
        self.org = org
        self.type_org = type_org
        self.position = position
    
    def save(self, advisor_email, report_types, creator_names):
        
        if not Advisor.exists(advisor_email):
            raise ValueError("Advisor does not exist")

        # Insert report
        query = '''INSERT INTO Report 
                  (title, intro, year, category, path, org, type_org, advisor_email, creator)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                  RETURNING report_id'''
        params = (self.title, self.intro, self.year, self.category, self.path,
                 self.org, self.type_org, advisor_email, session['user_id'])
        
        report_id = Database.execute_query(query, params, fetch=True)[0][0]
        
        # Insert authors
        for name in creator_names:
            query = '''INSERT INTO Author (au_id, name, report_id)
                       VALUES (%s, %s, %s)'''
            Database.execute_query(query, (session['au_id'], name, report_id))
        
        # Insert report types
        for type_id in report_types:
            query = '''INSERT INTO Re_type (report_id, type_id)
                       VALUES (%s, %s)'''
            Database.execute_query(query, (report_id, type_id))
        
        return report_id

''' Class Advisor '''    
class Advisor:
    @classmethod
    def exists(cls, email):
        query = "SELECT 1 FROM Advisor WHERE email = %s"
        return bool(Database.execute_query(query, (email,), fetch=True))
    
@app.route('/')
def index():
    return "Welcome to the website. Please <a href='/login_page'>login</a>."

@app.route('/login_page', methods=['GET'])
def login_page():
    return render_template('login.html')  # Ensure your template exists

''' Handle user login '''    
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    user = User.authenticate(email, password)
    
    if user:
        session['user_id'] = user.user_id
        session['email'] = user.email
        session['role'] = user.role
        session['au_id'] = user.au_id  
        
        if user.role == 'student':
            return redirect(url_for('Homepage_student'))
        elif user.role == 'teacher':
            return redirect(url_for('Homepage_teacher'))
    
    return redirect(url_for('Login_page'))

''' Show project for Homepage_student '''
@app.route('/Homepage_student')
def Homepage_student():
    conn = Database.connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT report_id, title, intro FROM report")
        projects = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return render_template("Homepage_student.html", projects=projects)

''' Show project for Homepage_teacher '''
@app.route('/Homepage_teacher')
def Homepage_teacher():
    conn = Database.connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT report_id, title, intro FROM report")
        projects = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return render_template("Homepage_teacher.html", projects=projects)


''' Read detail for ReadProject_page '''   
@app.route('/read_project/<int:report_id>')
def read_project(report_id):
    conn = Database.connect_db()
    cur = conn.cursor()
    try:
        # Get pdf_path from database
        cur.execute('SELECT path FROM report WHERE report_id = %s', (report_id,))
        report = cur.fetchone()
        
        if not report:
            return "Report not found", 404
        return render_template('ReadProject_page.html', pdf_path=report[0])
    finally:
        cur.close()
        conn.close()

''' Add Report '''
@app.route('/add_report', methods=['POST'])
def add_report():
    if session.get('role') != 'student':
        return redirect(url_for('Login_page'))

    try:
        # File upload handling
        pdf_file = request.files['path']
        if not pdf_file.filename.lower().endswith('.pdf'):
            raise ValueError("Only PDF file")
            
        filename = secure_filename(pdf_file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_file.save(pdf_path)

        # Get creator names
        num_creators = int(request.form['numCreators'])
        creator_names = [request.form[f'name_author{i}'] 
                        for i in range(1, num_creators+1)]
    
        # Create report
        report = Report(
            title=request.form['title'],
            intro=request.form['intro'],
            year=request.form['year'],
            category=request.form['category'],
            path=pdf_path,
            org=request.form.get('org'),
            type_org=request.form.get('type_org'),
            position=request.form.get('position')
        )

        # Save report
        report.save(
            advisor_email=request.form['name_advisor'],
            report_types=request.form.getlist('report_types[]'),
            creator_names=creator_names
        )
    
        return redirect(url_for('Homepage_student'))

    except Exception as e:
        return str(e), 400
    
''' Serve PDE '''
@app.route('/uploads/<filename>')
def get_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)