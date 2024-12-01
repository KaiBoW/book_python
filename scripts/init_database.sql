-- 创建数据库
CREATE DATABASE IF NOT EXISTS library_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE library_management;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    is_admin BOOLEAN DEFAULT FALSE,
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 班级表
CREATE TABLE IF NOT EXISTS classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    grade VARCHAR(32) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 学生表
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    student_id VARCHAR(32) NOT NULL UNIQUE,
    class_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 图书表
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    author VARCHAR(64),
    isbn VARCHAR(13) UNIQUE,
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    category VARCHAR(32),
    location VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 借阅表
CREATE TABLE IF NOT EXISTS borrowings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    student_id INT NOT NULL,
    borrow_date DATETIME NOT NULL,
    due_date DATETIME NOT NULL,
    return_date DATETIME,
    status VARCHAR(32) DEFAULT 'borrowed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建索引
CREATE INDEX idx_student_id ON students(student_id);
CREATE INDEX idx_isbn ON books(isbn);
CREATE INDEX idx_status ON borrowings(status);
CREATE INDEX idx_borrow_date ON borrowings(borrow_date);
CREATE INDEX idx_due_date ON borrowings(due_date);

-- 插入初始数据
INSERT INTO users (username, email, password_hash, is_admin, permissions) VALUES
('admin', 'admin@example.com', 
'scrypt:32768:8:1$B47Xfq3KSQ1oLi3N$afdc5619132bce347114d5e2300403a8b6152bfa8f97361d51a85169a1182be0bcab82c301b2cfd82eaa3f600c61205aa7c7b4237b0d6550c24e65fcc65ffe8b', 
TRUE, '{"user_manage": true, "book_manage": true, "class_manage": true, "student_manage": true}');

INSERT INTO classes (name, grade) VALUES
('一年级1班', '一年级'),
('二年级1班', '二年级');

INSERT INTO students (name, student_id, class_id) VALUES
('张三', '2024001', 1),
('李四', '2024002', 1);

INSERT INTO books (title, author, isbn, total_copies, available_copies, category, location) VALUES
('Python编程入门', '张教授', '9787111111111', 5, 5, '计算机', 'A区-01-01'),
('数学基础', '李教授', '9787111111112', 3, 3, '数学', 'B区-02-01'); 