from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.book import Book
from app.forms.book import BookForm, BookSearchForm
from app import db

bp = Blueprint('book', __name__)

@bp.route('/')
@login_required
def index():
    search_form = BookSearchForm()
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '')
    
    query = Book.query
    if keyword:
        query = query.filter(
            (Book.title.like(f'%{keyword}%')) |
            (Book.author.like(f'%{keyword}%')) |
            (Book.isbn.like(f'%{keyword}%'))
        )
    
    pagination = query.order_by(Book.id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    books = pagination.items
    
    return render_template('book/index.html', 
                         books=books, 
                         pagination=pagination,
                         search_form=search_form)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('book.index'))
    
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            total_copies=form.total_copies.data,
            available_copies=form.total_copies.data,
            category=form.category.data,
            location=form.location.data
        )
        db.session.add(book)
        try:
            db.session.commit()
            flash('图书添加成功', 'success')
            return redirect(url_for('book.index'))
        except:
            db.session.rollback()
            flash('图书添加失败，请检查ISBN是否重复', 'danger')
    
    return render_template('book/edit.html', form=form, title='添加图书')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('book.index'))
    
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        # 更新可用数量
        available_change = form.total_copies.data - book.total_copies
        book.total_copies = form.total_copies.data
        book.available_copies = book.available_copies + available_change
        book.category = form.category.data
        book.location = form.location.data
        
        try:
            db.session.commit()
            flash('图书更新成功', 'success')
            return redirect(url_for('book.index'))
        except:
            db.session.rollback()
            flash('图书更新失败，请检查ISBN是否重复', 'danger')
    
    return render_template('book/edit.html', form=form, title='编辑图书')

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if not current_user.is_admin:
        flash('权限不足', 'danger')
        return redirect(url_for('book.index'))
    
    book = Book.query.get_or_404(id)
    if book.borrowings.filter_by(status='borrowed').first():
        flash('该图书还有未归还的借阅记录，无法删除', 'danger')
        return redirect(url_for('book.index'))
    
    try:
        db.session.delete(book)
        db.session.commit()
        flash('图书删除成功', 'success')
    except:
        db.session.rollback()
        flash('图书删除失败', 'danger')
    
    return redirect(url_for('book.index')) 