from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, TextAreaField,
                     SelectField, DateField, FileField, FieldList, FormField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    dob = DateField("Date of Birth", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    province = StringField("Province/State/County", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    address = StringField("Residential Address", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    username = StringField("Username", validators=[DataRequired(), Length(min=4)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Repeat Password")
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class AcademicSubForm(FlaskForm):
    qualification = SelectField("Qualification", choices=[('High School','High School'),('Bachelors','Bachelor\'s'),('Masters','Masters')])
    field = StringField("Field of Study")
    institution = StringField("Institution Name")
    graduation = DateField("Graduation Date")

class StudentRegForm(FlaskForm):
    academics = FieldList(FormField(AcademicSubForm), min_entries=1, max_entries=5)
    transcript_file = FileField("Academic Transcript (PDF/DOC/DOCX)")
    exam_cert_file = FileField("National Exam Certificate (PDF/JPG/PNG)")
    diploma_file = FileField("Diploma/Degree Certificate (PDF/JPG/PNG)")
    occupation = StringField("Current Occupation")
    financial_info = TextAreaField("Financial Strength / Funding Details")
    submit = SubmitField("Submit Registration")

class InquiryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone (optional)")
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")