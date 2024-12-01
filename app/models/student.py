from app import db

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    student_id = db.Column(db.String(32), unique=True, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    borrowings = db.relationship('Borrowing', backref='student', lazy=True) 