from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Vote:
    db_name = 'PyPie_Derby'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']