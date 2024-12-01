from app import create_app, db
from app.models.user import User
from app.models.class_ import Class
from app.models.student import Student
from app.models.book import Book
from datetime import datetime

def init_db():
    app = create_app()
    with app.app_context():
        try:
            # 创建所有数据表
            print("开始创建数据表...")
            db.create_all()
            print("数据表创建成功！")

            # 检查是否已存在管理员用户
            if not User.query.filter_by(username='admin').first():
                print("创建管理员用户...")
                # 创建管理员用户
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True,
                    permissions={
                        'user_manage': True,
                        'book_manage': True,
                        'class_manage': True,
                        'student_manage': True
                    }
                )
                admin.set_password('admin123')
                db.session.add(admin)
                print("管理员用户创建成功！")

            # 创建测试班级
            print("创建测试班级...")
            class1 = Class(name='一年级1班', grade='一年级')
            class2 = Class(name='二年级1班', grade='二年级')
            db.session.add(class1)
            db.session.add(class2)

            # 创建测试学生
            print("创建测试学生...")
            student1 = Student(
                name='张三',
                student_id='2024001',
                class_id=1
            )
            student2 = Student(
                name='李四',
                student_id='2024002',
                class_id=1
            )
            db.session.add(student1)
            db.session.add(student2)

            # 创建测试图书
            print("创建测试图书...")
            book1 = Book(
                title='Python编程入门',
                author='张教授',
                isbn='9787111111111',
                total_copies=5,
                available_copies=5,
                category='计算机',
                location='A区-01-01'
            )
            book2 = Book(
                title='数学基础',
                author='李教授',
                isbn='9787111111112',
                total_copies=3,
                available_copies=3,
                category='数学',
                location='B区-02-01'
            )
            db.session.add(book1)
            db.session.add(book2)

            # 提交事务
            db.session.commit()
            print("所有测试数据创建成功！")

        except Exception as e:
            db.session.rollback()
            print(f"初始化数据库失败：{str(e)}")
            raise e

if __name__ == '__main__':
    try:
        init_db()
        print("数据库初始化完成！")
    except Exception as e:
        print(f"错误：{str(e)}") 