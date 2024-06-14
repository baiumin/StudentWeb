# -*- coding: utf-8 -*-
# time: 2023/6/18 10:09
# file: manage.py
# author: sober
import matplotlib
from flask import Flask, request, render_template, redirect, url_for
import pymysql
from matplotlib import pyplot as plt

app = Flask(__name__)

dbhost = '127.0.0.1'
dbuser = 'root'
dbpass = '123456'
dbname = 'flask'


def getStudents():
    # 打开数据库连接 主机地址  用户名 密码 数据库
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "select * from student"
    cursor.execute(sql)
    rows = cursor.fetchall()
    db.close()
    return rows


def getStudent(id):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "select * from student where id=" + str(id)
    cursor.execute(sql)
    row = cursor.fetchone()
    db.close()
    return row


@app.route('/')
def index():
    return redirect(url_for('user_login'))


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' or password == '':
            js_code = "<script>alert('请输入账号密码！'); history.back();</script>"
            return js_code

        user = get_user_by_username(username)
        if user:
            js_code = "<script>alert('用户已存在！'); history.back();</script>"
            return js_code
        else:
            register_db(username, password)
            return redirect(url_for('user_login'))


def register_db(username, password):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
    cursor.execute(sql, (username, password))
    db.commit()
    db.close()


def get_user_by_username(username):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM user WHERE username = %s"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()
    db.close()
    return user


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            js_code = "<script>alert('请输入账号密码！'); history.back();</script>"
            return js_code

        user = get_user_by_username(username)
        if user and user['password'] == password:
            return redirect(url_for('admin'))
        else:
            js_code = "<script>alert('登录失败！'); history.back();</script>"
            return js_code


@app.route('/admin', methods=['POST', 'GET'])  # 管理功能
def admin():
    students = getStudents()
    return render_template('admin.html', student=students)


@app.route('/home')
def home():
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    query = "select sex, count(*) from student group by sex"
    cursor.execute(query)
    data = cursor.fetchall()
    # 将查询结果转换为列表形式
    gender_data = [{'gender': row[0], 'count': row[1]} for row in data]
    cursor.close()
    db.close()
    # 提取性别列表和数量列表
    genders = [row['gender'] for row in gender_data]
    counts = [row['count'] for row in gender_data]
    explode = [0.1, 0]
    # 创建饼图
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(counts, labels=genders, autopct='%1.1f%%', explode=explode, shadow=True,
            textprops={'fontsize': 16, 'color': 'white'})
    plt.axis('equal')
    # 保存饼图为图片
    chart_path = 'static/chart.png'
    plt.savefig(chart_path, transparent=True)
    # 渲染模板并传递饼图路径
    return render_template('home.html', chart_path=chart_path)


@app.route('/add', methods=['GET', 'POST'])  # 添加学生
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        sex = request.form.get('sex')
        age = request.form.get('age')
        stu = getStudent(id)
        if id == "" or name == "" or sex == "" or age == "":
            js_code = "<script>alert('请填写完整信息！'); history.back();</script>"
            return js_code
        elif stu:
            js_code = "<script>alert('学生已存在！'); history.back();</script>"
            return js_code
        else:
            addstudent(id, name, sex, age)
            return redirect(url_for('admin'))


def addstudent(id, name, sex, age):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "insert into student (id,name,sex,age) values ('" + id + "','" + name + "','" + sex + "','" + age + "')"
    cursor.execute(sql)
    db.commit()
    db.close()


@app.route('/sort', methods=['GET'])  # 根据年龄排序
def sort():
    students = get_Sort_Students()
    return render_template('admin.html', student=students)


def get_Sort_Students():
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "select * from student order by  age asc"
    cursor.execute(sql)
    row = cursor.fetchall()
    db.close()
    return row


@app.route('/search', methods=['POST'])  # 查询学生
def search():
    if request.form.get('name') != '':  # 根据姓名查询
        name = request.form.get('name')
        students = searchstudents(name)
        return render_template('admin.html', student=students)
    elif request.form.get('id') != '':  # 根据学号查询
        id = request.form.get('id')
        students1 = searchstu1(id)
        return render_template('admin.html', student=students1)
    elif request.form.get('id') == '' and request.form.get('name') == '':
        js_code = "<script>alert('请输入查询内容！'); history.back();</script>"
        return js_code


def searchstudents(name):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "select * from student where name like '%" + name + "%'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row[1])
    db.close()
    return rows


def searchstu1(id):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = f"select * from student where id={id}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row[1])
    db.close()
    return rows


@app.route('/modify/<id>', methods=['GET', 'POST'])  # 修改学生
def modify(id):
    if request.method == 'GET':
        students = getStudents()
        editStudent = getStudent(id)
        id = editStudent[0]
        name = editStudent[1]
        sex = editStudent[2]
        age = editStudent[3]
        return render_template('modify.html', students=students, id=id, name=name, sex=sex, age=age)
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        sex = request.form.get('sex')
        age = request.form.get('age')
        if name == '' or sex == '' or age == '':
            js_code = "<script>alert('请输入修改信息！'); history.back();</script>"
            return js_code
        else:
            updateStudent(id, name, sex, age)
            return redirect(url_for('admin'))


def updateStudent(id, name, sex, age):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "update student set name='%s',sex='%s', age='%s' WHERE id=%s" % (name, sex, age, id)
    cursor.execute(sql)
    print(sql)
    db.commit()
    db.close()


@app.route('/delete/<id>', methods=['GET'])  # 删除学生
def delete(id):
    db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = db.cursor()
    sql = "delete from student where id=" + str(id)
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run('127.0.0.1', 5002, debug=True)
