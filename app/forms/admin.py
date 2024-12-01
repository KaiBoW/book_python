from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional

class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 120)])
    password = PasswordField('密码', validators=[Optional(), Length(6, 128)])
    is_admin = BooleanField('管理员权限')
    submit = SubmitField('提交')

class ClassForm(FlaskForm):
    name = StringField('班级名称', validators=[DataRequired(), Length(1, 64)])
    grade = StringField('年级', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField('提交')

class StudentForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 64)])
    student_id = StringField('学号', validators=[DataRequired(), Length(1, 32)])
    class_id = SelectField('班级', coerce=int, validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.class_id.choices = [(c.id, c.name) for c in Class.query.order_by(Class.name).all()] 