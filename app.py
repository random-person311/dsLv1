from datetime import timedelta
from flask import Flask, render_template, session, redirect, request, flash
import db

app = Flask(__name__)

app.secret_key = 'secret'
app.permanent_session_lifetime = timedelta(seconds=3600)


def guardPage(requireLogin, requireAdmin, destPage):
    if requireLogin:
        if 'user' not in session:
            return redirect('/login')
        if requireAdmin and session['role'] != 1:
            return redirect('/home')
    elif 'user' in session:
        return redirect('/home')
    return destPage

def isAdmin():
    return session['role'] == 1

def isLoggedIn():
    return 'user' in session

@app.route('/')
def index():
    if isLoggedIn():
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/login')
def login_page():
    if 'user' in session:
        return redirect('/home')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        session.pop('role')
    return redirect('/login')

@app.route('/register')
def register_page():
    if 'user' in session:
        return redirect('/home')
    return render_template('register.html')

@app.route('/register/submit', methods = ['POST'])
def register_submit():
    if isLoggedIn():
        return redirect('/home')
    if request.method == 'POST':
        data = request.form
        existingUser = db.get_user_by_name(data['username'])
        if existingUser != None:
            flash("This username is already used")
            return redirect('/register')

        db.add_user(data['username'], data['password'], 0)
        flash('Register successful')
        return redirect('/login')

@app.route('/auth', methods = ['POST'])
def auth():
    if 'user' in session:
        return redirect('/home')
    
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        role = db.auth(username, password)
        if role != None:
            session['user'] = username
            session['role'] = role
            return redirect('/home')
        else:
            flash("Incorrect username or password!")
            return redirect('/login')

@app.route('/dashboard_items.html')
def dashboard_items():
    return render_template('dashboard_items.html', data=[{
        'id':1,
        'name':'item1',
        'desc':'item1 desc',
        'category':'item1 category',
        'price':100.0,
        'stock':10
    }])


@app.route('/dashboard/items/edit/<id>')
def dashboard_items_edit(id):
    if session['role'] != 1:
        return redirect('/home')
    product = db.get_product(id)
    if product == None:
        return render_template('dashboard_edit_item.html', data=product)
    else:
        return redirect('/dashboard/items')









@app.route('/home')
def home():
    return guardPage(True, False, render_template('home.html'))