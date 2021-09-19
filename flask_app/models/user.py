from flask_app.config.mysqlconnection import connectToMySQL
import re  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls, form_data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL('PyPie_Derby').query_db(query, form_data)
        return results

    @staticmethod
    def register_validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 3:
            flash('First name must be at least 3 characters', "register")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash('Last name must be at least 3 characters', "register")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('PyPie_Derby').query_db(query, form_data)
        if len(results) != 0:
            flash('Email already exists. Please try logging in.', "register")
            is_valid = False
        if len(form_data['password']) < 8:
            flash('Password must be at least 8 characters', "register")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash('Passwords must match.', "register")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('PyPie_Derby').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('PyPie_Derby').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
