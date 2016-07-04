# Luke Kearney
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Define the blueprint: 'hello', set its url prefix: app.url/auth
mod_hello = Blueprint('hello', __name__, url_prefix='/hello')

# Set the route and accepted methods
@mod_hello.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')
