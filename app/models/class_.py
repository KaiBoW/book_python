from app import db

class Class(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    grade = db.Column(db.String(32), nullable=False)
    students = db.relationship('Student', backref='class_', lazy=True) 