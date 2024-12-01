import os
import pymysql
from config import Config

def init_database():
    try:
        # 连接MySQL（不指定数据库）
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=int(Config.MYSQL_PORT),
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        with conn.cursor() as cursor:
            print("开始初始化数据库...")
            
            # 读取SQL文件
            with open('scripts/init_database.sql', 'r', encoding='utf-8') as f:
                sql_commands = f.read()
            
            # 执行SQL命令
            for command in sql_commands.split(';'):
                if command.strip():
                    cursor.execute(command)
            
            conn.commit()
            print("数据库初始化成功！")
            print("\n管理员账号信息：")
            print("用户名：admin")
            print("密码：admin123")
            
    except Exception as e:
        print(f"数据库初始化失败：{str(e)}")
        raise e
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"错误：{str(e)}") 