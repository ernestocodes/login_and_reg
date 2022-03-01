import bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.confirm_password = db_data['confirm_password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        taters = bcrypt.generate_password_hash(data['password'])
        tots = bcrypt.generate_password_hash(data['confirm_password'])
        print(taters)
        user = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data ['email'],
            'password' : taters,
            'confirm_password' : tots,
        }
        query = "INSERT INTO users (first_name, last_name, email, password, confirm_password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(confirm_password)s, NOW(), NOW());"
        return connectToMySQL('login_users').query_db(query,user)

    @classmethod
    def log_in(cls, data):
        user = User.get_by_email(data)
        if not user:
            flash("Invalid email or password")
            return False
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash("Invalid email or password")
            return False
        return True

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('login_users').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )

    @classmethod
    def get_by_email (cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login_users').query_db(query,data)
        if results:
            return cls(results[0])
        return False

    @staticmethod
    def validate_reg(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter a correct email.")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must contain at least 2 characters.")
            is_valid = False
        if not f"{user['first_name']}".isalpha():
            flash("First name may only contain letters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must contain at least 2 characters.")
            is_valid = False
        if not f"{user['last_name']}".isalpha():
            flash("Last name may only contain letters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if  user['password'] != user['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid

