import pymysql

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ken711062',
    'database': 'mysql1',
}

# 获取数据库连接
def get_db_connection():
    return pymysql.connect(**db_config)

# 创建数据库表
def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))"
        cursor.execute(query)
        connection.commit()
        print("Table created successfully")
    except Exception as e:
        connection.rollback()
        print("Error creating table: " + str(e))
    finally:
        cursor.close()
        connection.close()

# 執行創建資料表的函式
create_table()
