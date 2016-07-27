# Luke Kearney
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app.app_forms.forms import SignupForm, LoginForm
from app.mod_db.models import User
from app import app
from app import db

mod_auth = Blueprint('mod_auth', __name__, url_prefix='/auth')
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'mod_auth.login'

# Set the route and accepted methods
@mod_auth.route('/hello', methods=['GET', 'POST'])
def hello():
    return "hello"


# @mod_auth.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()
#
#     if request.method == 'POST':
#         if form.validate() == False:
#             return render_template('auth/signup.html', form=form)
#         else:
#             user = User(form.email.data, form.password.data)
#             # newuser.create(email=form.email.date)
#             #user = User.create(email=form.email.data, password=form.password.data)
#             # db.session.add(newuser)
#             # db.session.commit()
#
#             #session['email'] = user.email
#
#             return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
#
#     elif request.method == 'GET':
#         return render_template('auth/signup.html', form=form)
#
@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    if user_logged_in:
        print("logged in")

    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('auth/login.html', form=form)
        else:
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user.check_password(form.password.data):
                print(user.id)
                login_user(user, remember=True)
                return redirect(url_for('mod_auth.hello'))

    elif request.method == 'GET':
        # check if the user session already exists
        # if 'email' in session:
        #     return session['email']
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