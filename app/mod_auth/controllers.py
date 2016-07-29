# Luke Kearney
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app.app_forms.forms import SignupForm, LoginForm
from app.mod_db.models import User
from flask_login import LoginManager, current_user
from flask_peewee.auth import Auth
from app import app

from app import auth_db
# auth = Auth(app, auth_db)

login_manager = LoginManager()
login_manager.init_app(app)

mod_auth = Blueprint('mod_auth', __name__, url_prefix='/auth')
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'mod_auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Set the route and accepted methods
@mod_auth.route('/hello', methods=['GET', 'POST'])
def hello():
    return "hello"


@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('auth/signup.html', form=form)
        else:
            # user = User(form.email.data, form.password.data)

            # newuser.create(email=form.email.date)
            #user = User.create(email=form.email.data, password=form.password.data)
            # db.session.add(newuser)
            # db.session.commit()

            #session['email'] = user.email

            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"

    elif request.method == 'GET':
        return render_template('auth/signup.html', form=form)
#
@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('auth/login.html', form=form)
        else:
            user = Auth.authenticate(form.email, form.password)
            if current_user.is_authenticated:
                # Auth.login_user(user)
                # redirect as appropriate
                return "logged in"
            else:
                return render_template('auth/login.html', form=form)

    elif request.method == 'GET':
        if current_user.is_authenticated:
            return "hello"
        else:
            return render_template('auth/login.html', form=form)
        pass
#
#     return render_template('auth/login.html', form=form)
#
#
# @mod_auth.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('mod_auth.login'))
#
#
# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(id)
#
# @mod_auth.route('/logcheck')
# @login_required
# def index():
#     return "you're logged in"