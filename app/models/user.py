from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import logging

logger = logging.getLogger(__name__)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.JSON)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        logger.debug(f"为用户 {self.username} 设置新的密码哈希: {self.password_hash}")

    def check_password(self, password):
        logger.debug(f"检查用户 {self.username} 的密码")
        logger.debug(f"存储的密码哈希: {self.password_hash}")
        result = check_password_hash(self.password_hash, password)
        logger.debug(f"密码验证结果: {'成功' if result else '失败'}")
        return result 