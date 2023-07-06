from flask import render_template, session,flash,redirect, request, url_for
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.model_users import User
from flask_app.models.model_recipes import Recipes
from flask_app.controllers import controller_users

@app.route('/recipes',methods=['GET'])
def get_recipes():
    if 'id' in session:
        list_recipes = Recipes.get_allrecipes_with_user()
        return render_template("recipes.html", list_recipes = list_recipes)
    return redirect('/')

@app.route('/recipes/new',methods=['GET'])
def new_recipe():
    if 'id' in session:
        return render_template("new_recipe.html")
    return redirect('/')      

@app.route('/recipes/new',methods=['POST'])
def post_new_recipe():
    data = {
        **request.form,
        "user_id": session['id']
    }
    if Recipes.validate_recipe(data) == False:
         return redirect('/recipes/new')
    else:
        id_recipe = Recipes.new_recipe(data)
        return redirect('/recipes')
    
@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
    data = {
        "id": id
    }
    Recipes.delete_one_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>',methods=['GET'])
def get_show_recipe(id):
    if 'id' in session:
        data = {
        "id": id
        }
        recipe = Recipes.show_one_recipe_with_user(data)
        return render_template("show_recipe.html", recipe = recipe)
    return redirect('/')  

@app.route('/recipes/edit/<int:id>',methods=['GET'])
def get_edit_recipe(id):
    if 'id' in session:
        data = {
        "id": id
        }
        recipe = Recipes.show_one_recipe(data)  
        return render_template("edit_recipe.html", recipe = recipe)
    return redirect('/')  

@app.route('/recipes/edit/<int:id>', methods = ['POST'])
def update_recipe(id):
    
    if Recipes.validate_recipe(request.form) == False:
         return redirect(f'/recipes/edit/{id}')
    else:
        data = {
            **request.form,
            "id": id
           
        }
        Recipes.update_one_recipe(data)
        return redirect('/recipes')
    