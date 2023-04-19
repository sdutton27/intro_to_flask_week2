from flask import Blueprint, flash, get_flashed_messages, render_template, request, redirect, url_for
#from app import app
from .forms import SignUpForm, LoginForm
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=["GET", "POST"])
def signupPage():
    # instantiate the form
    form = SignUpForm()
    # if the method is POST, do something
    #print(request.method)
    if request.method == 'POST':
        #print('valid post request made')
        if form.validate(): # if the form is valid, this is True
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            user = User.query.filter_by(username = username).first()
            if user:
                flash('That username is taken', 'danger')
                return render_template('signup.html', form = form)
            user = User.query.filter_by(email = email).first()
            if user:
                flash('That email is already in user. Please use another email', 'danger')
                return render_template('signup.html', form = form)

            user = User(username, email, password)
            #print(user)
            user.save_to_db() # helper method

            flash('Successfully created your account', 'success')

            return redirect(url_for('auth.loginPage'))

        else:
            flash('Invalid entry, please try again', 'danger')

    # if the method is GET
    return render_template('signup.html', form = form)


@auth.route('/login', methods=["GET", "POST"])
def loginPage():
    form = LoginForm()
    if request.method == "POST":
        if form.validate(): #if form is valid
            username = form.username.data
            password = form.password.data

            # what we want: SELECT * FROM user WHERE username=username
            # SQLAlchemy has a query that we can use
            # <table we want it from>.query.<method>
            # get() is only for primary key

            # we know that username is unique so this will only give us 1
            # but it will still return as a list so we have to do .first()
            user = User.query.filter_by(username=username).first()
            # method would go here if we were doing anything to user object
            

            # returns either the instance of the user of None
            if user: # user was found
                # verify password
                # looks at the password in the database = the password you sent in the form
                #if user.password == password:
                if check_password_hash(user.password, password):
                    # log in
                    login_user(user) #login the user
                    #print('log me in')

                    # take the user back to the homepage
                    return redirect(url_for('homePage'))
                else:
                    # invalid password
                    print('incorrect username(just for security) or password(true)')
            else: # user was not found
                print('incorrect username(true) or password(just for security)')

    return render_template('login.html', form = form)

@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    # we don't want a render_template here because it would need a form and that's hectic
    return redirect(url_for('auth.loginPage'))