# Luke Kearney
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextField, validators, SubmitField
from wtforms.validators import DataRequired, Email
from app.mod_auth.models import User

# class LoginForm(Form):
#     email = StringField('email', validators=[DataRequired(), Email])
#     password = PasswordField('password', validators=[DataRequired()])
#     remember_me = BooleanField('remember_me', default=True)


class SignupForm(Form):
    email = StringField("Email", [validators.DataRequired("Please enter an email address"),
                                  validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class LoginForm(Form):
    email = StringField("Email", [validators.DataRequired("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False