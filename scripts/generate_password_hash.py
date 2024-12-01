from werkzeug.security import generate_password_hash

# 生成密码哈希
password = 'admin123'
password_hash = generate_password_hash(password)
print(f"密码 '{password}' 的哈希值是:")
print(password_hash) 