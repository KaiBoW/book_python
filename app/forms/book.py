from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class BookForm(FlaskForm):
    title = StringField('书名', validators=[DataRequired(), Length(1, 128)])
    author = StringField('作者', validators=[DataRequired(), Length(1, 64)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(13, 13)])
    total_copies = IntegerField('总数量', validators=[DataRequired(), NumberRange(min=1)])
    category = StringField('分类', validators=[Optional(), Length(0, 32)])
    location = StringField('位置', validators=[Optional(), Length(0, 32)])
    submit = SubmitField('提交')

class BookSearchForm(FlaskForm):
    keyword = StringField('关键词', validators=[Optional()])
    submit = SubmitField('搜索') 