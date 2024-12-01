from app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(64))
    isbn = db.Column(db.String(13), unique=True)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    category = db.Column(db.String(32))
    location = db.Column(db.String(32))
    borrowings = db.relationship('Borrowing', backref='book', lazy=True) 