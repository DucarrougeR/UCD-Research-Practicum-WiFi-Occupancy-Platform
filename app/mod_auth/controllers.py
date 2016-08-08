# Luke Kearney
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app.app_forms.forms import SignupForm, LoginForm
from app.mod_db.models import User
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from app.values import strings
from app import app


# auth = Auth(app, auth_db)

login_manager = LoginManager()
login_manager.init_app(app)

mod_auth = Blueprint('mod_auth', __name__, url_prefix='/auth')
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'mod_auth.login'

@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.get(User.id == user_id)
        return user
    except Exception:
        print("uh oh")

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
            User.create_new(form.email.data, form.password.data)

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
            user = User.authenticate_user(form.email.data, form.password.data)
            if User.authenticate_user(form.email.data, form.password.data):
                if login_user(user):
                    print(current_user)
                    return "valid user"
                else:
                    return "error logging in"
            else:
                flash(strings.ERROR_LOGIN)
                return render_template('auth/login.html', form=form)

    elif request.method == 'GET':
        if current_user.is_authenticated:
            return "hello"
        else:
            return render_template('auth/login.html', form=form)
        pass

    return render_template('auth/login.html', form=form)


@mod_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mod_auth.login'))

@mod_auth.route('/logcheck')
@login_required
def index():
    print(current_user)
    return "you're logged in"