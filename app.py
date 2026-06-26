import sqlite3
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'admin'
csrf = CSRFProtect(app)

DB_FILE = "app.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            cid TEXT PRIMARY KEY,
            cname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()
init_db()

class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired('請輸入帳號')])
    password = PasswordField('密碼', validators=[DataRequired('請輸入密碼')])
    submit = SubmitField('登入')

class CustomerForm(FlaskForm):
    cid = StringField('客戶編號', validators=[
        DataRequired('客戶編號為必填欄位'),
        Length(min=3, max=10, message='編號長度需為 3~10 字元')
        ])
    cname = StringField('客戶姓名', validators=[DataRequired('客戶姓名為必填欄位')])
    email = StringField('電子郵件', validators=[DataRequired('Email 為必填欄位'),
        Email('請輸入有效的 Email 格式')
        ])
    phone = StringField('聯絡電話', validators=[
        DataRequired('電話為必填欄位'),
        Length(min=10, max=10, message='電話號碼必須為 10 碼')
        ])
    address = StringField('地址')
    submit = SubmitField('儲存')

@app.route('/')
def index():
    return render_template('index.html', title='首頁')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('customer_list'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin123':
            session['username'] = form.username.data
            return redirect(url_for('customer_list'))
        else:
            flash('帳號或密碼錯誤！')
            
    return render_template('login.html', form=form, title='管理員登入')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/customers')
def customer_list():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    conn.close()
    return render_template('customers.html', customers=customers, title='客戶列表')

@app.route('/customer/add', methods=['GET', 'POST'])
def customer_add():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    form = CustomerForm()
    if form.validate_on_submit():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO customer (cid, cname, email, phone, address) VALUES (?, ?, ?, ?, ?)",
                (form.cid.data, form.cname.data, form.email.data, form.phone.data, form.address.data)
            )
            conn.commit()
            flash('新增成功！')
            return redirect(url_for('customer_list'))
        except sqlite3.IntegrityError:
            flash('錯誤：客戶編號或 Email 已存在！')
        finally:
            conn.close()
            
    return render_template('customer_form.html', form=form, title="新增客戶", is_edit=False)

@app.route('/customer/<cid>/edit', methods=['GET', 'POST'])
def customer_edit(cid):
    if 'username' not in session:
        return redirect(url_for('login'))
        
    form = CustomerForm()
    
    if request.method == 'GET':
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer WHERE cid = ?", (cid,))
        customer = cursor.fetchone()
        conn.close()
        
        if not customer:
            flash('找不到該客戶資料！')
            return redirect(url_for('customer_list'))
            
        form.cid.data = customer['cid']
        form.cname.data = customer['cname']
        form.email.data = customer['email']
        form.phone.data = customer['phone']
        form.address.data = customer['address']

    elif form.validate_on_submit():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE customer SET cname=?, email=?, phone=?, address=? WHERE cid=?",
                (form.cname.data, form.email.data, form.phone.data, form.address.data, cid)
            )
            conn.commit()
            flash('修改成功！')
            return redirect(url_for('customer_list'))
        except sqlite3.IntegrityError:
            flash('錯誤：該 Email 已被其他客戶佔用！')
        finally:
            conn.close()
            
    return render_template('customer_form.html', form=form, title="編輯客戶", is_edit=True)

@app.route('/customer/<cid>/delete', methods=['POST'])
def customer_delete(cid):
    if 'username' not in session:
        return redirect(url_for('login'))
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer WHERE cid = ?", (cid,))
    conn.commit()
    conn.close()
    
    flash('刪除成功！')
    return redirect(url_for('customer_list'))

if __name__ == '__main__':
    app.run(debug=True)