import json, hashlib, os
from datetime import datetime
from flask import (render_template, flash, redirect, url_for, request,
                   current_app, send_from_directory)
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from . import db, mail
from .models import (User, StudentRegistration, Inquiry, Visitor,
                     Testimonial, PartnerUniversity)
from .forms import (RegistrationForm, LoginForm, StudentRegForm, InquiryForm)
from .email_util import send_inquiry_notification

ALLOWED_DOCS = {"pdf","doc","docx","jpg","jpeg","png"}


def save_file(file_storage):
    if not file_storage:
        return None
    ext = file_storage.filename.rsplit('.',1)[1].lower()
    if ext not in ALLOWED_DOCS:
        return None
    filename = datetime.utcnow().strftime('%Y%m%d%H%M%S_') + secure_filename(file_storage.filename)
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
    file_storage.save(upload_path)
    return filename

# visitor tracking

from . import create_app
app = create_app()

@app.before_request
def count_visitors():
    ip_hash = hashlib.sha256(request.remote_addr.encode()).hexdigest()
    visitor = Visitor.query.filter_by(ip_hash=ip_hash).first()
    if not visitor:
        visitor = Visitor(ip_hash=ip_hash)
        db.session.add(visitor)
        db.session.commit()

@app.context_processor
def inject_counts():
    return dict(total_visitors=Visitor.query.count(),
                admissions_count=StudentRegistration.query.count(),
                testimonial_count=Testimonial.query.count())

# routes

@app.route('/')
def index():
    testimonials = Testimonial.query.all()
    success_data = dict(
        scholarship_rate="92%",
        successful_admissions=StudentRegistration.query.count(),
        total_applicants=StudentRegistration.query.count()+50,  # example
        positive_reviews=Testimonial.query.count()
    )
    return render_template('index.html', testimonials=testimonials, success=success_data)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    dob=form.dob.data,
                    country=form.country.data,
                    province=form.province.data,
                    city=form.city.data,
                    address=form.address.data,
                    email=form.email.data,
                    username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    reg = StudentRegistration.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', registration=reg)

@app.route('/student/register', methods=['GET','POST'])
@login_required
def student_register():
    form = StudentRegForm()
    if form.validate_on_submit():
        data_json = json.dumps([{
            'qualification': a.qualification.data,
            'field': a.field.data,
            'institution': a.institution.data,
            'graduation': a.graduation.data.isoformat() if a.graduation.data else None
        } for a in form.academics])
        reg = StudentRegistration(
            user_id=current_user.id,
            academics_json=data_json,
            occupation=form.occupation.data,
            financial_info=form.financial_info.data,
            transcript_file=save_file(form.transcript_file.data),
            exam_cert_file=save_file(form.exam_cert_file.data),
            diploma_file=save_file(form.diploma_file.data)
        )
        db.session.add(reg)
        db.session.commit()
        flash('Student registration submitted successfully')
        return redirect(url_for('dashboard'))
    return render_template('student_register.html', form=form)

@app.route('/contact', methods=['GET','POST'])
def contact():
    form = InquiryForm()
    if form.validate_on_submit():
        inquiry = Inquiry(**{f.name: f.data for f in form})
        db.session.add(inquiry)
        db.session.commit()
        send_inquiry_notification(inquiry)  # optional email
        flash('Your message has been sent!')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/admissions')
def admissions():
    partners = PartnerUniversity.query.all()
    return render_template('admissions.html', partners=partners)

@app.route('/about')
def about():
    return render_template('about.html')

# serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(current_app.root_path,'static','uploads'), filename)