from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional
from datetime import datetime, timedelta
from app.models.book import Book
from app.models.student import Student

class BorrowingForm(FlaskForm):
    student_id = SelectField('学生', coerce=int, validators=[DataRequired()])
    book_id = SelectField('图书', coerce=int, validators=[DataRequired()])
    due_date = DateField('应还日期', validators=[DataRequired()], 
                        default=lambda: datetime.now() + timedelta(days=30))
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(BorrowingForm, self).__init__(*args, **kwargs)
        self.student_id.choices = [(s.id, f'{s.name} ({s.student_id})') 
                                 for s in Student.query.order_by(Student.name).all()]
        self.book_id.choices = [(b.id, f'{b.title} (可借: {b.available_copies})') 
                              for b in Book.query.filter(Book.available_copies > 0).order_by(Book.title).all()]

class BorrowingSearchForm(FlaskForm):
    keyword = StringField('关键词')
    status = SelectField('状态', choices=[
        ('', '全部'),
        ('borrowed', '借阅中'),
        ('returned', '已归还'),
        ('overdue', '逾期')
    ], validators=[Optional()])
    submit = SubmitField('搜索') 