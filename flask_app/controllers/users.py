from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template("account.html")

@app.route('/register', methods = ['POST'])
def register_account():
    if User.validate_reg(request.form):
        User.save(request.form)
        print(request.form)
        return redirect('/')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    print(request.form['email'])
    if User.log_in(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/')