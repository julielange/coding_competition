from flask import Flask, render_template, request, redirect
from sqlalchemy import ForeignKey, desc
from sqlalchemy.orm import relationship
from datetime import datetime
import requests
import json
from recipefinder.models import Search, Recipe, Instructions, Ingredients
from recipefinder import app
from recipefinder import db
import os


# home page
@app.route('/')
def index():
    return render_template('index.html')


# page to enter ingredients and send a request to spoonacular API
@app.route('/get_recipe', methods=['GET', 'POST'])
def get_recipe():
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        db.session.add(Search(ingredients=ingredients))
        db.session.commit()

        params = {"ingredients":ingredients,"number":"3","ranking":"2","ignorePantry":'true'}
        headers = {
            'x-rapidapi-host': os.getenv("RAPIDAPI_HOST"),
            'x-rapidapi-key': os.getenv("RAPIDAPI_KEY")
            }
        url = "https://rapidapi.p.rapidapi.com/recipes/findByIngredients"
        response = requests.request("GET", url, headers=headers, params=params)

        data = json.loads(response.text)

        for i in range(3):
            db.session.add(Recipe(title=data[i]['title'], number=data[i]['id'], image=data[i]['image']))
            db.session.commit()
        return redirect('/recipes')

    else:
        return render_template('get_recipe.html')
    

# page to list recipes found
@app.route('/recipes', methods=['GET', 'POST'])
def recommend_recipes():
    recipes = Recipe.query.order_by(Recipe.id.desc()).limit(3)
    recipes = recipes[::-1]
    return render_template('recipes.html', recipes=recipes)


# page to display recipe instructions and ingredients
@app.route('/recipes/instructions/<int:id>', methods=['GET', 'POST'])
def instructions(id):
    recipe = Recipe.query.get_or_404(id)
    recipe_name = recipe.title
    number = recipe.number

    # requesting ingredients
    url = "https://rapidapi.p.rapidapi.com/recipes/" + str(number) + "/ingredientWidget.json"
    headers = {
        'x-rapidapi-host': os.getenv("RAPIDAPI_HOST"),
        'x-rapidapi-key': os.getenv("RAPIDAPI_KEY")
    }
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)

    # saving ingredients in the database
    no_ingredients = len(data['ingredients'])
    for i in range(no_ingredients):
        db.session.add(Ingredients(number=number, name=data['ingredients'][i]['name'], amount=data['ingredients'][i]['amount']['metric']['value'], unit=data['ingredients'][i]['amount']['metric']['unit']))
        db.session.commit()
    
    ingr = Ingredients.query.order_by(Ingredients.id.desc()).limit(no_ingredients)


    # requesting instructions
    url = "https://rapidapi.p.rapidapi.com/recipes/" + str(number) + "/analyzedInstructions"
    querystring = {"stepBreakdown":"true"}
    headers = {
        'x-rapidapi-host': os.getenv("RAPIDAPI_HOST"),
        'x-rapidapi-key': os.getenv("RAPIDAPI_KEY")
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)

    # saving instructions in the database 
    total_steps = 0
    for i in range(len(data)):
        for x in data[i]['steps']: 
            db.session.add(Instructions(step=x['step'], step_no=x['number']))
            db.session.commit()
            total_steps = total_steps +1

    instr = Instructions.query.order_by(Instructions.id.desc()).limit(total_steps)
    instr = instr[::-1]
    return render_template('instructions.html', instructions=instr, ingredients=ingr, recipe_name=recipe_name)


# adding recipe to favourites
@app.route('/recipes/add_favourite/<int:id>', methods=['GET'])
def add_favourite(id):
    recipe = Recipe.query.get_or_404(id)
    recipe.favourite = True
    db.session.commit()
    return redirect('/recipes')


# page to list favourite recipes
@app.route('/favourites', methods=['GET'])
def favourites():
    fav = Recipe.query.filter(Recipe.favourite==True).all()
    return render_template('favourites.html', favourites=fav)


# deleting recipe from favourites
@app.route('/favourites/delete/<int:id>')
def delete_favourite(id):
    recipe = db.session.query(Recipe).filter(Recipe.id==id).first()
    recipe.favourite = False
    db.session.commit()
    return redirect('/favourites')
