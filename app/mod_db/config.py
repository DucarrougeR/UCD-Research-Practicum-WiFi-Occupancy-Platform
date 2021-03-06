
DEBUG = True
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = 'secret'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'
DATABASE = {
    'name': BASE_DIR + '/database.db',
    'engine': 'peewee.SqliteDatabase',
}
UPLOAD_FOLDER = BASE_DIR + '/app/static/uploads'
ALLOWED_EXTENSIONS = set(['zip', 'csv'])
DEFAULT_MAIL_SENDER = "hello@shittyapp.com"
