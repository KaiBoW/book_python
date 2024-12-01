from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.borrowing import Borrowing
from app.models.book import Book
from app.models.student import Student
from app.forms.borrowing import BorrowingForm, BorrowingSearchForm
from app import db
from datetime import datetime

bp = Blueprint('borrowing', __name__)

@bp.route('/')
@login_required
def index():
    search_form = BorrowingSearchForm()
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '')
    status = request.args.get('status', '')
    
    query = Borrowing.query
    if keyword:
        query = query.join(Book).join(Student).filter(
            (Book.title.like(f'%{keyword}%')) |
            (Student.name.like(f'%{keyword}%')) |
            (Student.student_id.like(f'%{keyword}%'))
        )
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(Borrowing.borrow_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    borrowings = pagination.items
    
    return render_template('borrowing/index.html', 
                         borrowings=borrowings, 
                         pagination=pagination,
                         search_form=search_form)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BorrowingForm()
    if form.validate_on_submit():
        book = Book.query.get(form.book_id.data)
        if book.available_copies <= 0:
            flash('该图书已无可借数量', 'danger')
            return redirect(url_for('borrowing.add'))
        
        borrowing = Borrowing(
            book_id=form.book_id.data,
            student_id=form.student_id.data,
            borrow_date=datetime.now(),
            due_date=form.due_date.data,
            status='borrowed'
        )
        book.available_copies -= 1
        
        try:
            db.session.add(borrowing)
            db.session.commit()
            flash('借阅记录添加成功', 'success')
            return redirect(url_for('borrowing.index'))
        except:
            db.session.rollback()
            flash('借阅记录添加失败', 'danger')
    
    return render_template('borrowing/edit.html', form=form, title='添加借阅')

@bp.route('/return/<int:id>')
@login_required
def return_book(id):
    borrowing = Borrowing.query.get_or_404(id)
    if borrowing.status == 'returned':
        flash('该图书已归还', 'warning')
        return redirect(url_for('borrowing.index'))
    
    borrowing.status = 'returned'
    borrowing.return_date = datetime.now()
    borrowing.book.available_copies += 1
    
    try:
        db.session.commit()
        flash('图书归还成功', 'success')
    except:
        db.session.rollback()
        flash('图书归还失败', 'danger')
    
    return redirect(url_for('borrowing.index'))

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('borrowing.index'))
    
    borrowing = Borrowing.query.get_or_404(id)
    if borrowing.status == 'borrowed':
        flash('借阅中的记录无法删除', 'danger')
        return redirect(url_for('borrowing.index'))
    
    try:
        db.session.delete(borrowing)
        db.session.commit()
        flash('借阅记录删除成功', 'success')
    except:
        db.session.rollback()
        flash('借阅记录删除失败', 'danger')
    
    return redirect(url_for('borrowing.index'))

# 定时任务：更新逾期状态
def update_overdue_status():
    now = datetime.now()
    overdue_borrowings = Borrowing.query.filter(
        Borrowing.status == 'borrowed',
        Borrowing.due_date < now
    ).all()
    
    for borrowing in overdue_borrowings:
        borrowing.status = 'overdue'
    
    try:
        db.session.commit()
    except:
        db.session.rollback()

@bp.route('/students/<int:id>/borrowings')
@login_required
def student_borrowings(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('main.index'))
    
    student = Student.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    # 修改查询方式
    pagination = Borrowing.query.filter_by(student_id=id)\
        .order_by(Borrowing.borrow_date.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    borrowings = pagination.items
    return render_template('admin/student_borrowings.html', 
                         student=student, 
                         borrowings=borrowings, 
                         pagination=pagination) 