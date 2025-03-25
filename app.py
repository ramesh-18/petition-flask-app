from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/petition'  # Update credentials if needed
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB file limit

# Initialize Database
db = SQLAlchemy(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Keyword-based Department Mapping
DEPARTMENT_KEYWORDS = {
    "Revenue Department": ["land", "property tax", "mutation", "patta", "chitta"],
    "Social Welfare Department": ["pension", "disability", "widow", "scholarship"],
    "Rural Development": ["village", "panchayat", "rural", "scheme"],
    "Urban Development": ["municipality", "city", "town", "urban", "metro"],
    "Engineering Department": ["road", "bridge", "electricity", "water"],
    "Agriculture-related Departments": ["farming", "crop", "fertilizer", "loan"],
    "Education Department": ["school", "college", "student", "admission"],
    "Health Departments": ["hospital", "doctor", "medicine", "clinic"],
    "Police Department": ["crime", "theft", "FIR", "harassment"],
    "Cooperative Department": ["loan", "cooperative", "bank", "finance"],
    "Registration Department": ["marriage", "land registration", "document"],
    "Public Welfare": ["military", "veteran", "ex-servicemen"],
    "Pension Directorate": ["pension", "retirement", "benefits"],
    "Hindu Religious and Charitable Endowments": ["temple", "trust", "donation"],
    "Tamil Nadu Housing Board": ["housing", "flat", "real estate"],
    "Judiciary": ["court", "case", "lawyer", "judge"],
    "Welfare of Differently Abled Persons": ["disability", "handicapped", "aid"],
    "Tamil Nadu Slum Clearance Board": ["slum", "rehabilitation", "eviction"],
    "Survey and Settlement Department": ["survey", "boundary", "land measurement"],
    "Handloom and Textiles Department": ["textile", "weaving", "loom"],
    "Land Administration Department": ["land", "dispute", "survey"]
}

# Function to determine department based on keywords
def get_department(petition_details):
    petition_text = petition_details.lower()
    for department, keywords in DEPARTMENT_KEYWORDS.items():
        if any(keyword in petition_text for keyword in keywords):
            return department
    return "Unknown Department"

# ------------- Database Models -------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    petitions = db.relationship('Petition', backref='user', lazy=True)

class Petition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    petition_type = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=False)
    applicant_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    door_number = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    taluk = db.Column(db.String(100), nullable=False)
    revenue_village = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# ------------- Routes -------------
@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        new_user = User(
            fullname=request.form['fullname'],
            email=request.form['email'],
            password=hashed_pw,
            phone=request.form['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        try:
            details = request.form['details']
            department = get_department(details)

            new_petition = Petition(
                user_id=user.id,
                user_type=request.form['user_type'],
                department=department,
                petition_type=request.form['petition_type'],
                details=details,
                applicant_name=request.form['applicant_name'],
                phone=request.form['phone'],
                gender=request.form['gender'],
                door_number=request.form['door_number'],
                street=request.form['street'],
                area=request.form['area'],
                district=request.form['district'],
                taluk=request.form['taluk'],
                revenue_village=request.form['revenue_village']
            )
            db.session.add(new_petition)
            db.session.commit()
            flash(f'Petition submitted to {department}', 'success')
        except Exception as e:
            flash(f"[ERROR] Petition submission failed: {e}", "danger")
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('login'))

# ------------- Run the App -------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
