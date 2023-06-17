from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# 資料庫連線設定
db_config = {
    'host': '0.0.0.0',
    'user': 'root',
    'password': 'password',
    'database': 'mysql1',
}

# 取得資料庫連線
def get_db_connection():
    return pymysql.connect(**db_config)

# 建立使用者
@app.route('/create', methods=['POST'])
def create_user():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "INSERT INTO users (name, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, password, email))
        connection.commit()
        return redirect('/users')
    except Exception as e:
        connection.rollback()
        return 'Error creating user: ' + str(e)
    finally:
        cursor.close()
        connection.close()

# 刪除使用者
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        return redirect('/users')
    except Exception as e:
        connection.rollback()
        return 'Error deleting user: ' + str(e)
    finally:
        cursor.close()
        connection.close()

# 更改密碼頁面
@app.route('/change_password/<int:user_id>', methods=['GET'])
def change_password_page(user_id):
    return render_template('change_password.html', user_id=user_id)

# 更改密碼
@app.route('/change_password/<int:user_id>', methods=['POST'])
def change_password(user_id):
    new_password = request.form['new_password']

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(query, (new_password, user_id))
        connection.commit()
        return redirect('/users')
    except Exception as e:
        connection.rollback()
        return 'Error changing password: ' + str(e)
    finally:
        cursor.close()
        connection.close()

# 取得使用者列表
@app.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        query = "SELECT id, name, email FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        return render_template('index.html', users=users)
    except Exception as e:
        return 'Error retrieving users: ' + str(e)
    finally:
        cursor.close()
        connection.close()

# 根路由，導向使用者列表
@app.route('/')
def root():
    return redirect('/users')

if __name__ == '__main__':
    app.run(port=5001)
