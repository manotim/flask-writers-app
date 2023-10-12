from flask_wtf import FlaskForm

from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, Length, NumberRange
from writingapp.models import Auth


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    role = StringField('Role',
                           validators=[DataRequired(), Length(min=2, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Auth.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another email')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Auth.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another email')


class JobForm(FlaskForm):
    assignment_type = SelectField('Assignment Type', choices=[
        ('Article review', 'Article review'),
        ('Article writing', 'Article writing'),
        ('Coding Assignment', 'Coding Assignment'),
        ('Programming Project', 'Programming Project'),
        ('Software Development', 'Software Development'),
        ('Web Development', 'Web Development'),
        ('Admission essay', 'Admission essay')
    ], validators=[InputRequired()])
    
    service = SelectField('Service', choices=[
        ('Copy editing', 'Copy editing'),
        ('Programming', 'Programming'),
        ('Proofreading', 'Proofreading'),
        ('Research assistance', 'Research assistance')
    ], validators=[InputRequired()])
    education_level = SelectField('Education Level', choices=[
        ('School', 'School'),
        ('University', 'University'),
        ('College', 'College'),
        ("Master's", "Master's"),
        ('Doctorate', 'Doctorate')
    ], validators=[InputRequired()])
    
    complexity = SelectField('Complexity', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], validators=[InputRequired()])
    
    number_of_pages = IntegerField('Number Of Pages', validators=[InputRequired(), NumberRange(min=1)])
    number_of_words = IntegerField('Number Of Words', validators=[InputRequired(), NumberRange(min=275)])
    
    line_spacing = SelectField('Line Spacing', choices=[
        ('single', 'Single'),
        ('double', 'Double')
    ], validators=[InputRequired()])
    assignment_language = SelectField('Assignment Language', choices=[
        ('English(US)', 'English(US)'),
        ('English(UK)', 'English(UK)'),
        ('Spanish(ES)', 'Spanish(ES)'),
        ('French(FR)', 'French(FR)')
    ], validators=[InputRequired()])
    
    sources_required = SelectField('Sources Required', choices=[
        ('Not specified', 'Not specified'),
        ('1 source required', '1 source required'),
        # Add all other source options here
    ], validators=[InputRequired()])
    
    citation_style = SelectField('Citation Style', choices=[
        ('APA 6th edition', 'APA 6th edition'),
        ('APA 7th edition', 'APA 7th edition'),
        # Add other citation styles here
    ], validators=[InputRequired()])
    subject = SelectField('Subject', choices=[
        ('Nursing', 'Nursing'),
        ('Front-End Development', 'Front-End Development'),
        ('Mobile App Development', 'Mobile App Development'),
        ('Other', 'Other')
    ], validators=[InputRequired()])
    
    instructions = TextAreaField('Instructions', validators=[InputRequired()])
    
    deadline = DateField('Deadline', validators=[InputRequired()])
    submit_date = DateField('Submission Date', validators=[InputRequired()])
    job_amount = DecimalField('Job Amount', places=2, render_kw={'readonly': True})
    
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Auth.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
