from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app.models.user import User
from app.forms.auth import LoginForm
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        logger.debug(f"尝试登录用户名: {form.username.data}")
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None:
            logger.warning(f"用户名不存在: {form.username.data}")
            flash('用户名或密码错误', 'danger')
            return redirect(url_for('auth.login'))
        
        logger.debug(f"找到用户: {user.username}, ID: {user.id}")
        logger.debug(f"数据库中的密码哈希: {user.password_hash}")
        
        if not user.check_password(form.password.data):
            logger.warning(f"密码验证失败，用户: {user.username}")
            flash('用户名或密码错误', 'danger')
            return redirect(url_for('auth.login'))
        
        logger.info(f"用户登录成功: {user.username}")
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logger.info(f"用户登出: {current_user.username}")
    logout_user()
    flash('您已成功退出登录', 'success')
    return redirect(url_for('main.index')) 