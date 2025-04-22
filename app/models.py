from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_hash = db.Column(db.String(128), unique=True, nullable=False)
    first_visit = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    dob = db.Column(db.Date)
    country = db.Column(db.String(64))
    province = db.Column(db.String(64))
    city = db.Column(db.String(64))
    address = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class StudentRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # academic details (json blob for flexibility)
    academics_json = db.Column(db.Text)  # store as JSON string

    occupation = db.Column(db.String(128))
    financial_info = db.Column(db.Text)

    transcript_file = db.Column(db.String(256))
    exam_cert_file = db.Column(db.String(256))
    diploma_file = db.Column(db.String(256))

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(32))
    subject = db.Column(db.String(128))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(64))
    text = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1‑5
    photo = db.Column(db.String(256))

class PartnerUniversity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text)
    fall_deadline = db.Column(db.String(64))
    spring_deadline = db.Column(db.String(64))
    process_overview = db.Column(db.Text)