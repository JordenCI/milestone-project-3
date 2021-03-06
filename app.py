import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_site'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)


"""Home page displays all recipes stored"""
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html", recipes=mongo.db.recipes.find())

"""User Login Form"""
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})
        if login_user:
            if request.form['password'] == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            flash('Invalid username/password combination')
    return render_template('login.html')

"""User registration Form"""
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        users = mongo.db.users
        existing_user = users.find_one({"username": request.form['username']})

        if existing_user is None:
            users.insert_one(request.form.to_dict())
            session['username'] = request.form['username']
            return redirect(url_for("index"))

        flash('That username already exists! Please choose another')

    return render_template("register.html")

"""User logout"""
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

"""Add a recipe"""
@app.route('/add_recipe')
def add_recipe():
    return render_template(
        'addrecipe.html',
        recipes=mongo.db.recipes.find(),
        categories=mongo.db.categories.find(),
        cuisine=mongo.db.cuisine.find(),
        serving_size=mongo.db.serving_size.find(),
        difficulty=mongo.db.difficulty.find(),
        user=session['username'])

"""Add new category to database"""
@app.route('/add_new_category', methods=['POST'])
def add_new_category():
    category_name = mongo.db.categories
    if request.method == "POST":
        for i in request.form:
            if i == "edit":
                category_name.insert_one({'category_name': request.form['category_name']})
                print(request.referrer)
                return redirect(request.referrer)
            if i == "add":
                category_name.insert_one({'category_name': request.form['category_name']})
                return redirect(url_for('add_recipe'))
    return redirect(url_for('add_recipe'))

"""Add new cuisine to database"""
@app.route('/add_new_cuisine', methods=['POST'])
def add_new_cuisine():
    cuisine_type = mongo.db.cuisine
    if request.method == "POST":
        for i in request.form:
            if i == "edit":
                cuisine_type.insert_one({'cuisine_type': request.form['cuisine_type']})
                print(request.referrer)
                return redirect(request.referrer)
            if i == "add":
                cuisine_type.insert_one({'cuisine_type': request.form['cuisine_type']})
                return redirect(url_for('add_recipe'))
    
    return redirect(url_for('add_recipe'))

"""Add new recipe to database"""
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('index'))

"""Add new contact request to database"""
@app.route('/contact_requests', methods=['POST'])
def contact_requests():
    requests = mongo.db.contact_requests
    requests.insert_one(request.form.to_dict())
    return redirect(url_for('index'))

"""Displays detailed recipe page by ID"""
@app.route('/recipes/<item_id>')
def recipes(item_id):
    recipe = mongo.db.recipes
    recipe.find_one_and_update({'_id': ObjectId(item_id)}, {'$inc': {'views': 1}})
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(item_id)})
    return render_template('recipes.html', recipes=the_recipe)

"""Checks if user created recipe, if so they may edit, if not, redirect to index"""
@app.route('/edit_recipe/<recipes_id>')
def edit_recipe(recipes_id):
    if "username" in session:
        username = session["username"]
        the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipes_id)})
        recipe_detail = mongo.db.recipes.find()
        if the_recipe['username'] == username:
            return render_template('editrecipe.html', recipes=the_recipe, detail=recipe_detail, recipes1=mongo.db.recipes.find(), categories=mongo.db.categories.find(), cuisine=mongo.db.cuisine.find(), serving_size=mongo.db.serving_size.find(), difficulty=mongo.db.difficulty.find())
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

"""Updates database with new information"""
@app.route('/update_recipe/<recipes_id>', methods=['POST'])
def update_recipe(recipes_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipes_id)},
    {
        'recipe_name': request.form['recipe_name'],
        'image': request.form['image'],
        'description': request.form['description'],
        'category_name': request.form['category_name'],
        'cuisine_type': request.form['cuisine_type'],
        'prep_time': request.form['prep_time'],
        'cook_time': request.form['cook_time'],
        'serving_size': request.form['serving_size'],
        'difficulty': request.form['difficulty'],
        'date_added': request.form['date_added'],
        'username': request.form['username'],
        'ingredients_1': request.form['ingredients_1'],
        'ingredients_2': request.form['ingredients_2'],
        'ingredients_3': request.form['ingredients_3'],
        'ingredients_4': request.form['ingredients_4'],
        'ingredients_5': request.form['ingredients_5'],
        'ingredients_6': request.form['ingredients_6'],
        'ingredients_7': request.form['ingredients_7'],
        'ingredients_8': request.form['ingredients_8'],
        'ingredients_9': request.form['ingredients_9'],
        'ingredients_10': request.form['ingredients_10'],
        'method_1': request.form['method_1'],
        'method_2': request.form['method_2'],
        'method_3': request.form['method_3'],
        'method_4': request.form['method_4'],
        'method_5': request.form['method_5'],
        'method_6': request.form['method_6'],
        'method_7': request.form['method_7'],
        'method_8': request.form['method_8'],
        'method_9': request.form['method_9'],
        'method_10': request.form['method_10']

    })
    return redirect(url_for('index'))

"""Checks if user created recipe, if so they may delete from database, if not, redirect to index"""
@app.route('/delete_recipe/<recipes_id>')
def delete_recipe(recipes_id):
    if "username" in session:
        username = session["username"]
        the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipes_id)})
        if the_recipe['username'] == username:
            mongo.db.recipes.remove({'_id': ObjectId(recipes_id)})
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


"""Text input search"""
@app.route('/search', methods=['GET', 'POST'])
def search():
    q = request.args.get("search", "")
    query = ({"$text": {"$search": q}})
    results = mongo.db.recipes.find(query)
    cur = results
    x = []
    for i in cur:
        x.append(i)
    return render_template('searchresults.html', recipes=x)


"""Starter filter"""
@app.route('/starter')
def starter_filter():
    query = ({"$text": {"$search": "starter"}})
    results = mongo.db.recipes.find(query)
    cur = results
    x = []
    for i in cur:
        x.append(i)
    return render_template('starterfilter.html', recipes=x)


"""Breakfast filter"""
@app.route('/breakfast')
def breakfast_filter():
    query = ({"$text": {"$search": "breakfast"}})
    results = mongo.db.recipes.find(query)
    cur = results
    x = []
    for i in cur:
        x.append(i)
    return render_template('breakfastfilter.html', recipes=x)


"""Lunch filter"""
@app.route('/lunch')
def lunch_filter():
    query = ({"$text": {"$search": "lunch"}})
    results = mongo.db.recipes.find(query)
    cur = results
    x = []
    for i in cur:
        x.append(i)
    return render_template('lunchfilter.html', recipes=x)


"""Dinner filter"""
@app.route('/dinner')
def dinner_filter():
    query = ({"$text": {"$search": "dinner"}})
    results = mongo.db.recipes.find(query)
    cur = results
    x = []
    for i in cur:
        x.append(i)
    return render_template('dinnerfilter.html', recipes=x)


"""Dessert filter"""
@app.route('/dessert')
def dessert_filter():
    query = ({"$text": {"$search": "dessert"}})
    results = mongo.db.recipes.find(query)
    cur = results
    x = []
    for i in cur:
        x.append(i)
    return render_template('dessertfilter.html', recipes=x)

"""Most viewed filter"""
@app.route('/most_viewed')
def views():
    recipes = mongo.db.recipes.find().sort([('views', DESCENDING)])
    return render_template('index.html', recipes=recipes)

"""Most recent filter"""
@app.route('/most_recent')
def date_added():
    recipes = mongo.db.recipes.find().sort([('date_added', DESCENDING)])
    return render_template('index.html', recipes=recipes)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP',),
            port=int(os.environ.get('PORT')),
            debug=False)
