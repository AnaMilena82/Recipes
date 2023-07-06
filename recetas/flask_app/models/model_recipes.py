from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.model_users import User
from flask_app import app,BASE_DE_DATOS
from flask import flash
import math

class Recipes:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.elaboration_date = db_data['elaboration_date']
        self.uder_30min = db_data['uder_30min']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = None

    
    @classmethod
    def new_recipe(cls,data):
        query = """INSERT INTO recipes (name,description,instructions,elaboration_date, uder_30min,user_id)
                 VALUES (%(name)s,%(description)s,%(instructions)s, %(elaboration_date)s, %(uder_30min)s, %(user_id)s);"""
        id_recipe = connectToMySQL(BASE_DE_DATOS).query_db(query,data)
        return id_recipe

    @classmethod
    def get_allrecipes_with_user(cls):
        query = """
                SELECT * 
                FROM recipes r JOIN users u
                ON r.user_id = u.id;    
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query)
        list_recipes = []
        for row in result:
            recipe = Recipes(row)
            data_user = {
                "id":row['u.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['u.created_at'],
                "updated_at":row['u.updated_at']
            }
            user = User (data_user)
            recipe.user = user
            list_recipes.append(recipe)
        return list_recipes

    @classmethod
    def delete_one_recipe(cls, data):
        query = """
                DELETE 
                FROM recipes 
                WHERE id = %(id)s;    
                """
        return connectToMySQL(BASE_DE_DATOS).query_db(query, data)

    @classmethod
    def show_one_recipe_with_user(cls, data):
        query = """
                SELECT * 
                FROM recipes r JOIN users u
                ON r.user_id = u.id
                WHERE r.id = %(id)s;     
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        row = result [0]
        recipe = Recipes (row)
        data_user = {
                "id":row['u.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['u.created_at'],
                "updated_at":row['u.updated_at']
        }
        recipe.user = User(data_user)
        return recipe 

    @classmethod  
    def show_one_recipe(cls, data):
        query = """
                SELECT * 
                FROM recipes 
                WHERE id = %(id)s;     
                """
        result = connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        recipe = Recipes (result [0])
        return recipe

    @classmethod  
    def update_one_recipe(cls, data):
        query = """
                UPDATE recipes 
                SET name = %(name)s,description = %(description)s,instructions = %(instructions)s,elaboration_date =  %(elaboration_date)s, uder_30min = %(uder_30min)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(BASE_DE_DATOS).query_db(query, data)  
        


    @staticmethod
    def validate_recipe( data ):
        is_valid = True

        if len( data['name'] ) < 3:
            is_valid = False
            flash( "You need to provide the name of the recipe.", "error_name" )
        if len( data['description'] ) < 3:
            is_valid = False
            flash( "You need to provide the descriptión of the recipe.", "error_description" )
        if len( data['instructions'] ) < 3:
            is_valid = False
            flash( "You need to provide the Instructions of the recipe.", "error_instructions" )
        if data['elaboration_date'] == "":
            is_valid = False
            flash( "You need to provide the Elaboration Date of the recipe.", "error_elaborationdate" )
        if "uder_30min" not in data:
            is_valid = False
            flash( "You need to provide if the recipe takes less than 30 minutes.", "error_uder30min" )
        
        
        return is_valid
    