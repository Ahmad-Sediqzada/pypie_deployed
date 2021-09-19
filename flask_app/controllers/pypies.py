from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.pypie import PyPie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/create/pypie', methods = ['POST'])
def create_pypie():
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    form_data = {
        "name": request.form['name'], 
        'filling': request.form['filling'], 
        'crust': request.form['crust'],
        'user_id': session['user_id']
    }
    PyPie.create_pypie(form_data)
    return redirect('/dashboard')

@app.route('/destroy/pypie/<int:id>')
def destroy_pypie(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    PyPie.destroy_pypie(data)
    return redirect('/dashboard')

@app.route('/show/pypie')
def show_pypie():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template('show_pypie.html', user = User.get_by_id(data), pypies = PyPie.show_all_pypie())

@app.route('/edit/pypie/<int:id>')
def edit_pypie(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    return render_template('edit_pypie.html', edit_pypie = PyPie.get_one(data))

@app.route('/update/pypie/<int:post_id>', methods=['POST'])
def update_pypie(post_id):
    PyPie.update_pypie(request.form)
    return redirect('/dashboard')

@app.route('/display/<int:id>')
def display(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id

    }
    user_data = {
        "id": session['user_id']
    }
    return render_template('display.html', pypie = PyPie.get_one(data), vote_pie = PyPie.get_all_user_voted_pies(user_data))


@app.route('/vote/<int:id>')
def like(id):
    data = {
        "user_id": session['user_id'],
        "pypie_id": id
        }
    PyPie.vote(data)
    return redirect('/show/pypie') 