# My First Coding Competition
This project is part of a coding competition held by [IT-Talents](https://www.it-talents.de).
It showcases a solution to find suitable recipes with ingredients you already have at home. 
<br>
<br>

**Features:**
* Enter ingredients you like to use for cooking
* Recommendation of 3 suitable recipes
* Save your favourite recipes 
* Get detailled steps and ingredient lists
<br>
<br>

**Technologies used:**
* Python 3.8
* Flask web framework 
* SQLight database with SQL Alchemy
* Spoonacular API to access recipes
<hr>

**Installation:**
1. Check if Python 3.8 is installed
2. Install all packages listed in requirements.txt
3. Get registered at [Rapid API](https://rapidapi.com/spoonacular/api/recipe-food-nutrition) and sign up for the free plan of Spoonacular API
4. Save credentials as environment variables (you can use [python-dotenv](https://pypi.org/project/python-dotenv/) and create a seperate .env file)
5. Alternatively, hard code your credentials in file "route.py" in line 29/30, line 64/65 and line 83/84
6. Use your command line to access the folder "what_is_in_my_fridge" and enter `python3 run.py`
7. Port 5000 on local host will be opended and the programm is ready to be used in your browser
