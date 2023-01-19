from wtforms.validators import Email
from library     import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id            = db.Column(db.Integer(),primary_key=True)
    username      = db.Column(db.String(length=30),nullable=False,unique=True)
    email         = db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash = db.Column(db.String(length=100),nullable=False,unique=True)
    type          = db.Column(db.String(length=10),nullable=False)
    items         = db.relationship('BookItem',backref='owned_user',lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_message):
        self.password_hash = bcrypt.generate_password_hash(plain_text_message).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
class BookItem(db.Model):
    id            = db.Column(db.Integer(),primary_key=True)
    title         = db.Column(db.String(length=250),nullable=False,unique=True)
    description   = db.Column(db.String(length=1000),nullable=False)
    genre         = db.Column(db.String(length=30),nullable=False)
    author        = db.Column(db.String(length=30),nullable=False)
    stocks        = db.Column(db.Integer(),nullable=False)
    owner         = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def __repr__(self) -> str:
        return f'BookItem {self.title}'

class Borrower(db.Model):
    id            = db.Column(db.Integer(),primary_key=True)
    username      = db.Column(db.String(length=50))
    book_title    = db.Column(db.String(length=250))
    email         = db.Column(db.String(length=50))
    date_borrowed = db.Column(db.Date())
    date_returned = db.Column(db.Date())
