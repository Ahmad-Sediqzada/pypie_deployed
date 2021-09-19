from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, vote
from flask import flash

class PyPie:

    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.filling = db_data['filling']
        self.crust = db_data['crust']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creater = None
        self.users_who_voted = []

    @classmethod
    def get_all_pypie(cls):
        query = "SELECT * FROM PyPies"
        results = connectToMySQL('PyPie_Derby').query_db(query)
        return results

    @classmethod
    def vote(cls, data):
        query = "INSERT INTO votes (user_id, pypie_id) VALUES (%(user_id)s, %(pypie_id)s);"
        results = connectToMySQL('PyPie_Derby').query_db(query, data)
        return results

    @classmethod
    def get_all_user_voted_pies(cls, data):
        pies_voted = []
        query = "SELECT PyPie_id FROM votes JOIN users ON users.id = user_id WHERE user_id = %(id)s"
        results = connectToMySQL('PyPie_Derby').query_db(query, data)
        for result in results:
            pies_voted.append(result['PyPie_id'])
        return pies_voted

    @classmethod
    def show_all_pypie(cls):
        query = "SELECT * FROM PyPies "\
        "LEFT JOIN users ON users.id = PyPies.user_id "\
        "LEFT JOIN votes ON votes.pypie_id = PyPies.id "\
        "LEFT JOIN users AS users2 ON users2.id = votes.user_id "\
        "ORDER BY PyPies.created_at DESC"

        results = connectToMySQL('PyPie_Derby').query_db(query)
        all_pypies = []

        for result in results:
            new_pypie = True
            vote_user_data = {
                "id": result['users2.id'],
                "first_name": result['users2.first_name'], 
                "last_name": result['users2.last_name'],
                "email": result['users2.email'],
                "password": result['users2.password'],
                "created_at": result['users2.created_at'],
                "updated_at": result['users2.updated_at']
            }
            if len(all_pypies) > 0 and all_pypies[len(all_pypies) -1].id == result['id']:
                all_pypies[len(all_pypies) -1].users_who_voted.append(user.User(vote_user_data))
                new_pypie = False

            if new_pypie:
                pypie = cls(result)
                creater_data = {
                    "id": result['users.id'],
                    "first_name": result['first_name'], 
                    "last_name": result['last_name'],
                    "email": result['email'],
                    "password": result['last_name'],
                    "created_at": result['created_at'],
                    "updated_at": result['updated_at']
                    }
                pypie.creater = user.User(creater_data)

                if result['users2.id'] is not None:
                    pypie.users_who_voted.append(user.User(vote_user_data))
                all_pypies.append(pypie)
        return all_pypies

    @classmethod 
    def create_pypie(cls, form_data):
        query = "INSERT INTO PyPies (name, filling, crust, user_id) VALUES (%(name)s, %(filling)s, %(crust)s, %(user_id)s);"
        results = connectToMySQL('PyPie_Derby').query_db(query, form_data)
        return results

    @classmethod
    def destroy_pypie(cls, data):
        query = "DELETE FROM PyPies WHERE id = %(id)s"
        results = connectToMySQL('PyPie_Derby').query_db(query, data)
        return results

    @classmethod
    def show_pypie(cls, data):
        query = "SELECT * FROM PyPies WHERE id = %(id)s"
        results = connectToMySQL('PyPie_Derby').query_db(query, data)
        return results[0]

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM PyPies WHERE id = %(id)s"
        results = connectToMySQL('PyPie_Derby').query_db(query, data)
        return cls(results[0])


    @classmethod
    def update_pypie(cls, data):
        query = "UPDATE PyPies SET name = %(name)s, filling = %(filling)s, crust = %(crust)s WHERE id = %(id)s;"
        results = connectToMySQL('PyPie_Derby').query_db(query, data)
