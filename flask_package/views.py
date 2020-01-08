from flask import render_template, request,redirect,url_for,flash
from flask_package.forms import RegistrationForm, LoginForm
from flask_package.models import User, Blog
from flask_package import app,db,bcrypt
from flask_login import login_user, logout_user, current_user,login_required
from logging import DEBUG
from werkzeug.urls import url_parse
from datetime import datetime

app.logger.setLevel(DEBUG)
   


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register',methods =['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email = form.email.data,password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Registraion Successfull !!')
        return redirect(url_for('login'))
    elif form.errors:
        flash("Registration unsuccessful. Please try again")
        return redirect(url_for('register'))
    return render_template('register.html',title='register',form=form)


#The @before_request decorator from Flask register the decorated function to be executed right before the view function.
#This is extremely useful because now I can insert code that I want to execute before any view function in the application, and I can have it in a single place
@app.before_request
def before_request():                    
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/login',methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            #If we access /post without being logged in then @login_required dec redirects us to login page, By doing this, it will add a query string 'next' argument to this URL i.e. URL /login?next=/post
            #here after login we directly want to access /post so next_page variable will have '/post' value
            next_page = request.args.get('next')
            #if next_page is empty that means normal login and next_page is /profile not /post since we are logging in
            if not next_page or url_parse(next_page).netloc != '':
                next_page=url_for('profile',user_name=user.username)
            return redirect(next_page)
            flash('Login Successful ')
            app.logger.debug('Login successful for user: ' + user.username)
    elif form.errors:
        return redirect(url_for('login'))
    return render_template('login.html',title='login',form=form)


@app.route('/logout')
def logout():
     logout_user()
     return redirect(url_for('index'))

@app.route('/post',methods=['GET','POST'])
@login_required #This decorator makes this function protected and will not allow access to users that are not authenticated.You have to login to access /post.
#You will be redirected to /login page as coded in init.py
def posts():
    if request.method == "POST":
        UserText = request.form['msg']
        pst = Blog(post = UserText,usernamep=current_user.username)
        db.session.add(pst)
        db.session.commit()
        mypst = Blog.query.filter_by(usernamep=current_user.username).all()
    else:
        mypst = Blog.query.filter_by(usernamep=current_user.username).all()
    return render_template('feedback.html', mypst = mypst)


@app.route('/profile/<user_name>')
def profile(user_name):
    last_seen = current_user.last_seen
    #about_me = current_user.about_me
    return render_template('profile.html',name=user_name,last_seen = last_seen)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.shell_context_processor
def make_shell_context():
    return{'db':db, 'User':User,'Blog':Blog}
