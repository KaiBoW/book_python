from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.class_ import Class
from app.models.student import Student
from app.forms.admin import UserForm, ClassForm, StudentForm
from app import db
from app.models.borrowing import Borrowing

bp = Blueprint('admin', __name__)

@bp.route('/')
@login_required
def index():
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin/index.html')

# 用户管理
@bp.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    users = pagination.items
    return render_template('admin/users.html', users=users, pagination=pagination)

# 班级管理
@bp.route('/classes')
@login_required
def classes():
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    pagination = Class.query.order_by(Class.id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    classes = pagination.items
    return render_template('admin/classes.html', classes=classes, pagination=pagination)

# 学生管理
@bp.route('/students')
@login_required
def students():
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    pagination = Student.query.order_by(Student.id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    students = pagination.items
    return render_template('admin/students.html', students=students, pagination=pagination)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=form.is_admin.data,
            permissions={
                'user_manage': form.is_admin.data,
                'book_manage': True,
                'class_manage': form.is_admin.data,
                'student_manage': form.is_admin.data
            }
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('用户添加成功', 'success')
            return redirect(url_for('admin.users'))
        except:
            db.session.rollback()
            flash('用户添加失败，可能用户名或邮箱已存在', 'danger')
    
    return render_template('admin/user_edit.html', form=form, title='添加用户')

@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        user.permissions = {
            'user_manage': form.is_admin.data,
            'book_manage': True,
            'class_manage': form.is_admin.data,
            'student_manage': form.is_admin.data
        }
        
        if form.password.data:
            user.set_password(form.password.data)
        
        try:
            db.session.commit()
            flash('用户更新成功', 'success')
            return redirect(url_for('admin.users'))
        except:
            db.session.rollback()
            flash('用户更新失败，可能用户名或邮箱已存在', 'danger')
    
    return render_template('admin/user_edit.html', form=form, title='编辑用户')

@bp.route('/users/delete/<int:id>')
@login_required
def delete_user(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    if id == current_user.id:
        flash('不能删除当前登录用户', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('用户删除成功', 'success')
    except:
        db.session.rollback()
        flash('用户删除失败', 'danger')
    
    return redirect(url_for('admin.users'))

@bp.route('/classes/add', methods=['GET', 'POST'])
@login_required
def add_class():
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    form = ClassForm()
    if form.validate_on_submit():
        class_ = Class(
            name=form.name.data,
            grade=form.grade.data
        )
        try:
            db.session.add(class_)
            db.session.commit()
            flash('班级添加成功', 'success')
            return redirect(url_for('admin.classes'))
        except:
            db.session.rollback()
            flash('班级添加失败', 'danger')
    
    return render_template('admin/class_edit.html', form=form, title='添加班级')

@bp.route('/classes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_class(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    class_ = Class.query.get_or_404(id)
    form = ClassForm(obj=class_)
    
    if form.validate_on_submit():
        class_.name = form.name.data
        class_.grade = form.grade.data
        try:
            db.session.commit()
            flash('班级更新成功', 'success')
            return redirect(url_for('admin.classes'))
        except:
            db.session.rollback()
            flash('班级更新失败', 'danger')
    
    return render_template('admin/class_edit.html', form=form, title='编辑班级')

@bp.route('/classes/delete/<int:id>')
@login_required
def delete_class(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    class_ = Class.query.get_or_404(id)
    has_students = Student.query.filter_by(class_id=id).first() is not None
    
    if has_students:
        flash('该班级还有学生，无法删除', 'danger')
        return redirect(url_for('admin.classes'))
    
    try:
        db.session.delete(class_)
        db.session.commit()
        flash('班级删除成功', 'success')
    except:
        db.session.rollback()
        flash('班级删除失败', 'danger')
    
    return redirect(url_for('admin.classes'))

@bp.route('/classes/<int:id>/students')
@login_required
def class_students(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    class_ = Class.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = Student.query.filter_by(class_id=id)\
        .order_by(Student.id.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    students = pagination.items
    return render_template('admin/class_students.html', 
                         class_=class_, 
                         students=students, 
                         pagination=pagination)

@bp.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            student_id=form.student_id.data,
            class_id=form.class_id.data
        )
        try:
            db.session.add(student)
            db.session.commit()
            flash('学生添加成功', 'success')
            return redirect(url_for('admin.students'))
        except:
            db.session.rollback()
            flash('学生添加失败，可能学号已存在', 'danger')
    
    return render_template('admin/student_edit.html', form=form, title='添加学生')

@bp.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    
    if form.validate_on_submit():
        student.name = form.name.data
        student.student_id = form.student_id.data
        student.class_id = form.class_id.data
        try:
            db.session.commit()
            flash('学生信息更新成功', 'success')
            return redirect(url_for('admin.students'))
        except:
            db.session.rollback()
            flash('学生信息更新失败，可能学号已存在', 'danger')
    
    return render_template('admin/student_edit.html', form=form, title='编辑学生')

@bp.route('/students/delete/<int:id>')
@login_required
def delete_student(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    student = Student.query.get_or_404(id)
    from app.models.borrowing import Borrowing
    has_active_borrowings = Borrowing.query.filter_by(
        student_id=id, 
        status='borrowed'
    ).first() is not None
    
    if has_active_borrowings:
        flash('该学生还有未归还的图书，无法删除', 'danger')
        return redirect(url_for('admin.students'))
    
    try:
        db.session.delete(student)
        db.session.commit()
        flash('学生删除成功', 'success')
    except:
        db.session.rollback()
        flash('学生删除失败', 'danger')
    
    return redirect(url_for('admin.students'))

@bp.route('/students/<int:id>/borrowings')
@login_required
def student_borrowings(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    student = Student.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = Borrowing.query.filter_by(student_id=id)\
        .order_by(Borrowing.borrow_date.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    borrowings = pagination.items
    return render_template('admin/student_borrowings.html', 
                         student=student, 
                         borrowings=borrowings, 
                         pagination=pagination) 