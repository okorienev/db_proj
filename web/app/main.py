from flask import Flask
from .extensions import db, login_manager, User, ExtensionType
from .config import Config
from hashlib import sha512

app = Flask(__name__)
app.config.from_object(Config)
login_manager.init_app(app)
db.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


def create_admin():
    admin = User(login=Config.admin_login,
                 password=sha512(Config.admin_pass.encode()).hexdigest(),
                 email=Config.admin_email)
    db.session.add(admin)
    db.session.commit()


def create_ext_types():
    types = [
        {'type_name': 'Text', 'type_shortened': 'txt',
         'type_description': 'Extension type to represent large block of text'},
        {'type_name': 'Image', 'type_shortened': 'img',
         'type_description': 'Extension type to represent images'},
        {'type_name': 'String', 'type_shortened': 'str',
         'type_description': 'Extension type to represent single-line text'},
    ]
    for i in types:
        new_type = ExtensionType(**i)
        db.session.add(new_type)
    db.session.commit()


@app.before_first_request
def before_first_request():
    db.create_all()  # creating database, will not attempt to re-create tables
    if User.query.count() == 0:
        create_admin()
    if ExtensionType.query.count() == 0:
        create_ext_types()
