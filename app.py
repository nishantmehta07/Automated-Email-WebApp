from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from email_sender import send_bulk_emails
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")  # Secure key for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=hashed_pw
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except:
            flash('User already exists.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        sender_password = request.form['sender_password']
        subject = request.form['subject']
        body = request.form['body']
        raw_recipients = request.form['recipients'].split(',')

        # Format recipient list
        recipients = [(email.strip(), "Company", email.strip()) for email in raw_recipients]

        try:
            send_bulk_emails(sender_email, sender_password, recipients, subject, body)
            flash('Emails sent successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
