import re

from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASWORD_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    db_name = "mvcusersmagazines"

    def __init__(self, data):
        self.id = data["user_id"]
        self.firstName = data["firstName"]
        self.lastName = data["lastName"]
        self.email = data["email"]
        self.password = data["password"]
        self.confirmPassword = data["confirmPassword"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users where id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (firstName, lastName, email, password) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE users set firstName = %(firstName)s, lastName = %(lastName)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address!", "emailLogin")
            is_valid = False
        if len(user["password"]) < 1:
            flash("Password is required!", "passwordLogin")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_userRegister(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address!", "emailRegister")
            is_valid = False
        if len(user["password"]) < 1:
            flash("Password is required!", "passwordRegister")
            is_valid = False
        if len(user["firstName"]) < 1:
            flash("First name is required!", "nameRegister")
            is_valid = False
        if len(user["lastName"]) < 1:
            flash("Last name is required!", "lastNameRegister")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_userUpdate(user):
        is_valid = True
        if len(user["firstName"]) < 1:
            flash("First name is required!", "nameRegister")
            is_valid = False
        if len(user["lastName"]) < 1:
            flash("Last name is required!", "lastNameRegister")
            is_valid = False
        return is_valid
