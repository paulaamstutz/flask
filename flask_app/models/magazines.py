from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


class Magazine:
    db_name = "mvcusersmagazines"

    def __init__(self, data):
        self.id = data["magazine_id"]
        self.title = data["title"]
        self.description = data["description"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data):
        query = "INSERT INTO magazines (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM magazines;"
        results = connectToMySQL(cls.db_name).query_db(query)
        magazines = []
        if results:
            for magazine in results:
                magazines.append(magazine)
        return magazines

    @classmethod
    def get_magazine_by_id(cls, data):
        query = "SELECT * FROM magazines LEFT JOIN users on magazines.user_id = users.id WHERE magazines.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            comments = []
            query2 = "SELECT * FROM comments left join users on comments.user_id = users.id where comments.magazines_id = %(id)s;"
            result2 = connectToMySQL(cls.db_name).query_db(query2, data)
            if result2:
                for comment in result2:
                    comments.append(comment)
            result[0]["comments"] = comments
            query3 = "SELECT users.firstName, users.lastName FROM likes left join users on likes.user_id = users.id where likes.magazines_id = %(id)s;"
            result3 = connectToMySQL(cls.db_name).query_db(query3, data)
            likes = []
            if result3:
                for like in result3:
                    likes.append(like)
            result[0]["likes"] = likes
            return result[0]
        return False

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM magazines where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE magazines set description = %(description)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO likes (user_id, magazine_id) VALUES (%(user_id)s, %(magazine_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query = "DELETE FROM likes WHERE magazine_id=%(magazine_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_users_who_liked_by_magazine_id(cls, data):
        query = "SELECT user_id FROM likes where magazine_id = %(magazine_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        usersId = []
        if results:
            for userId in results:
                usersId.append(userId["user_id"])
        return usersId

    @staticmethod
    def validate_magazine(magazine):
        is_valid = True
        if len(magazine["title"]) < 2:
            flash("Title should be more  or equal to 2 characters", "title")
            is_valid = False
        if len(magazine["description"]) < 10:
            flash(
                "Description should be more  or equal to 10 characters", "description"
            )
            is_valid = False

        return is_valid

    @staticmethod
    def validate_magazineUpdate(magazine):
        is_valid = True
        if len(magazine["description"]) < 10:
            flash(
                "Description should be more  or equal to 10 characters", "description"
            )
            is_valid = False
        if len(magazine["nrOfPages"]) < 1:
            flash("Number of pages is required", "nrOfPages")
            is_valid = False
        if len(magazine["price"]) < 1:
            flash("Price is required", "price")
            is_valid = False
        return is_valid
