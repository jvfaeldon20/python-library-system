from flask            import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = '490e1373029bcafce42fdbd6'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from library import routes
