from flask import render_template, url_for, flash, redirect, request
from writingapp import app, db, bcrypt, mail
from writingapp.forms import (RegistrationForm, LoginForm, 
                              UpdateAccountForm, JobForm,
                              RequestResetForm, ResetPasswordForm)
from writingapp.models import Auth, Job
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.paginate(page=page, per_page=2)
    return render_template('home.html', jobs=jobs)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Auth(email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Auth.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember=form.remember.data)
           next_page = request.args.get('next')
           return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route('/job/new', methods=['GET', 'POST'])
@login_required
def new_job():
    form = JobForm()
    
    if form.validate_on_submit():
        job = Job(
            complexity=form.complexity.data, 
            deadline=form.deadline.data,
            assignment_type=form.assignment_type.data,
            service=form.service.data,
            education_level=form.education_level.data,
            number_of_pages=form.number_of_pages.data,
            number_of_words=form.number_of_words.data,
            line_spacing=form.line_spacing.data,
            assignment_language=form.assignment_language.data,
            sources_required=form.sources_required.data,
            citation_style=form.citation_style.data,
            subject=form.subject.data,
            instructions=form.instructions.data,
            submit_date=form.submit_date.data,
            amount=43.53,
            )
        db.session.add(job)
        db.session.commit()
        flash('You have added a new assignment successfully!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors, "Errors in the form")
    return render_template('create_job.html', title='New Job', form=form)



@app.route('/job/<int:job_id>')
def show_job(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job.html', job=job)

@app.route("/job/<string:by_service>")
def similar_jobs(by_service):
    page = request.args.get('page', 1, type=int)
    job = Job.query.filter_by(service=by_service).first_or_404()
    jobs = Job.query.filter_by(service=job.service).paginate(page=page, per_page=2)
    return render_template('similar_jobs.html', jobs=jobs, job=job)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='adventistmike@gmail.com', 
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: 
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Auth.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Auth.verify_reset_token(token)
    if user in None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)