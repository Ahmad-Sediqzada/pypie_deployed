from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.pypie import PyPie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register/user', methods=['POST'])
def register():

    if not User.register_validator(request.form):
        return redirect('/')
    data = { 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.register_user(data)
    return redirect('/dashboard')

        
@app.route('/dashboard')
def dashboard():
    data = {
        "id": session['user_id']
    }
    return render_template('/dashboard.html', user = User.get_by_id(data), pypies = PyPie.get_all_pypie())
    

@app.route('/user/login', methods=['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password.', "login")
        return redirect('/home')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password.')
        return redirect('/home')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/new/pypie')
def new_pypie():
    return render_template('create_pypie.html')