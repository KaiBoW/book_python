# 📚 图书管理系统

基于 Flask 的图书管理系统，提供图书管理、借阅管理、班级管理、学生管理等功能。

## ✨ 主要功能

- 🔑 **用户管理**：多角色用户系统，权限控制
- 📖 **图书管理**：图书信息维护，库存管理
- 🔄 **借阅管理**：借阅、归还、续借、逾期处理
- 👥 **班级管理**：班级信息维护，学生分班管理
- 👨‍🎓 **学生管理**：学生信息维护，借阅记录追踪

## 🛠️ 技术栈

- 🔹 **后端**：Flask + MySQL + SQLAlchemy
- 🔹 **前端**：Bootstrap + jQuery
- 🔹 **工具**：Python 3.8+, pip, Git

## 🚀 快速开始

### 1️⃣ 克隆项目并安装依赖

克隆项目：

```bash
git clone https://github.com/KaiBoW/book_python.git
cd library-management
```
创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
安装依赖：
```bash
pip install -r requirements.txt
```
### 2️⃣ 配置数据库
```bash
CREATE DATABASE library_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 config.py：
```python
MYSQL_USER = 'your_username'
MYSQL_PASSWORD = 'your_password'
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
```
### 3️⃣ 初始化系统
初始化数据库：
```bash
python scripts/init_database.py
```
运行应用：
```bash
python run.py
```

### 4️⃣ 访问系统
- 🌐 地址：[http://localhost:5000](http://localhost:5000)
- 👤 管理员账号：admin
- 🔒 管理员密码：admin123



### 📞 联系方式
- 👨‍💻 作者：质量不太守恒
- 📧 邮箱：[wangkaibo33@hotmail.com](mailto:wangkaibo33@hotmail.com)
- 🔗 项目：[https://github.com/KaiBoW/book_python.git](https://github.com/KaiBoW/book_python.git)
- 🟢 微信：ddouu3

## 📄 许可证
- MIT License

⭐ 如果这个项目对你有帮助，欢迎 Star！

