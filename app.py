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

@app.route('/dashboard/items', methods = ['GET'])
def dashboard_items():
    products = db.get_products()
    return render_template('dashboard_items.html', data=products)




@app.route('/dashboard/items/edit/<id>')
def dashboard_items_edit(id):
    if session['role'] != 1:
        return redirect('/home')
    product = db.get_product(id)
    if product == None:
        return render_template('dashboard_edit_item.html', data=product)
    else:
        return redirect('/dashboard/items')


@app.route('/dashboard/users')
def dashboard_users():
    if session['role'] != 1:
        return redirect('/home')
    users = db.get_users()
    return render_template('usersOverview.html', data=users)

@app.route('/dashboard/users/edit/<id>')
def dashboard_users_edit(id):
    if session['role'] != 1:
        flash("You don't have permission to access this page!")
        return redirect('/home')
    user = db.get_users()
    if user == None:
        return render_template('dashboard_edit_user.html', data=user)
    else:
        return redirect('/dashboard/users')

@app.route('/dashboard/users/sumbitedit/<id>', methods = ['POST'])
def save_user_edit(id):
    if not isAdmin():
        flash("You don't have permission to access this page!")
        return redirect('/home')
    if request.method == 'POST':
        data = request.form
        db.update_user(id, data)
        flash(f'Saved  changes to {data["username"]}')
        return redirect('/dashboard/users')
    
@app.route('/dashboard/users/delete/<id>')
def delete_user(id):
    if not isAdmin():
        flash("You don't have permission to access this page!")
        return redirect('/home')
    db.delete_user(id)
    flash('User deleted')
    return redirect('/dashboard/users')

@app.route('/profit')
def profit():
    return guardPage(True, False, render_template('profit.html', data=db.get_user_purchases(session['user'])))

@app.route('/home')
def home():
    return guardPage(True, False, render_template('home.html'))