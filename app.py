import os
from flask import request, render_template, redirect, flash, Flask, session, g, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Cookbook, Recipe, Ingredient, Instruction, CustomIngredient
from forms import LoginForm, SignUpForm, AddCookbookForm, AddRecipeForm, BuildSearchForm, BuildTagForm, BuildNotesForm, RecipeQuickAdd

CURR_USER_KEY = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///home_cook_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "devsecret")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    session[CURR_USER_KEY] = user.id


def do_logout():
    """logout user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        return True
    else:
        return False


@app.route('/')
def home_page():
    if g.user:
        return redirect(f'/users/{g.user.id}')
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}")
            return redirect('/')
        flash('Invalid credentials')

    return render_template('/login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    if do_logout():
        return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                full_name=form.full_name.data,
                profile_pic=form.profile_pic.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username is already taken!")
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect('/')

    return render_template('signup.html', form=form)


@app.route('/users/<int:user_id>')
def user_landing_page(user_id):
    selected_user = User.query.get(user_id)
    recipe_count=0
    cookbooks = selected_user.cookbooks
    for cookbook in cookbooks:
        recipe_count += len(cookbook.recipes)
    return render_template('main.html', cookbooks=cookbooks, recipe_count=recipe_count)

@app.route('/recipes/build')
def recipe_from_scratch():
    new_recipe = Recipe(name='New Recipe', cookbook_id = None, user_id=g.user.id)
    db.session.add(new_recipe)
    db.session.commit()     # figure out a way to not have to commit if recipe is cancelled?
    return redirect(f'/recipes/{new_recipe.id}/edit')

@app.route('/recipes/<int:recipe_id>/edit', methods = ['GET'])
def view_and_edit_recipe(recipe_id):
    selected_recipe = Recipe.query.get(recipe_id)
    main_recipe_form = AddRecipeForm(name=selected_recipe.name, cookbook=selected_recipe.cookbook_id)
    main_recipe_form.cookbook.choices = [(cookbook.id, cookbook.name)
                             for cookbook in Cookbook.query.filter_by(user_id=g.user.id)]
    build_search_form = BuildSearchForm()
    build_tag_form = BuildTagForm()
    build_notes_form = BuildNotesForm()
    return render_template('recipe.html', recipe=selected_recipe,
                            main_recipe_form=main_recipe_form,
                              build_search_form=build_search_form,
                                build_tag_form=build_tag_form,
                                  build_notes_form=build_notes_form)



@app.route('/users/<int:user_id>/cookbooks/<int:cookbook_id>/add_recipe', methods=['POST'])
def add_new_recipe(user_id, cookbook_id):
    form = RecipeQuickAdd()
    form.recipe.choices = [(recipe.id, recipe.name)
                             for recipe in Recipe.query.all()]
    if form.validate_on_submit():
        recipe_to_add = Recipe.query.get(form.recipe.data)
        recipe_to_add.cookbook_id = cookbook_id
        db.session.add(recipe_to_add)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        return redirect(f'/user/{user_id}')


@app.route('/users/<int:user_id>/cookbooks/add', methods=['GET', 'POST'])
def add_new_cookbook(user_id):
    form = AddCookbookForm()
    if form.validate_on_submit():
        name = form.name.data
        new_cookbook = Cookbook(name=name, user_id=user_id)
        db.session.add(new_cookbook)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    return render_template('add_cookbook.html', form=form)

@app.route('/users/<int:user_id>/profile')
def profile_view(user_id):
    selected_user = User.query.get(user_id)
    return render_template('profile.html', user=selected_user)

@app.route('/cookbooks/<int:cookbook_id>')
def view_cookbook(cookbook_id):
    selected_cookbook = Cookbook.query.get(cookbook_id)
    return render_template('cookbook.html', cookbook=selected_cookbook)


#******************************************************************************
# API routes

@app.route('/api/recipes/<int:recipe_id>/edit/info')
def send_recipe_data(recipe_id):
    selected_recipe = Recipe.query.get(recipe_id)
    return jsonify(recipe=selected_recipe.serialize())


@app.route('/api/recipes/<int:recipe_id>/edit/<string:ingredient_name>/add', methods = ['POST'])
def add_ingredient_to_recipe(recipe_id, ingredient_name):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.json['ingredient_type'] == 'standard':
        ingredient = Ingredient.query.filter_by(name=ingredient_name).one()
        if ingredient:
            recipe.child_ingredients.append(ingredient)
            db.session.commit()
            return f'success'
        return 'not ingredient'
    elif request.json['ingredient_type'] == 'custom':
        custom_ingredient = CustomIngredient(name=ingredient_name, recipe_id = recipe_id)
        db.session.add(custom_ingredient)
        db.session.commit()
        return 'success'
    else:
        return 'failed to add ingredient'

@app.route('/api/recipes/<int:recipe_id>/edit/delete', methods =['POST'])
def delete_ingredient(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.json['ingredient_type'] == 'standard':
        ingredient_name = request.json['ingredient_name']
        ingredient = Ingredient.query.filter_by(name=ingredient_name).one()
    if ingredient:
        recipe.child_ingredients.remove(ingredient)
        db.session.commit()
        return 'success'
    return 'failure'

@app.route('/api/recipes/<int:recipe_id>/edit/save', methods = ['POST'])
def save_recipe(recipe_id):
    main_recipe_form = AddRecipeForm()
    main_recipe_form.cookbook.choices = [(cookbook.id, cookbook.name)
                             for cookbook in Cookbook.query.filter_by(user_id=g.user.id)]
    selected_recipe = Recipe.query.get(recipe_id)
    # save recipe name and cookbook data, redirect to user form
    # The ingredients data is saved as they are added, and so do  not need to be saved here
    if main_recipe_form.validate_on_submit():
        name = main_recipe_form.name.data
        cookbook_id = main_recipe_form.cookbook.data
        selected_recipe.name = name
        selected_recipe.cookbook_id = cookbook_id
        db.session.add(selected_recipe)
        db.session.commit()
        return redirect(f'/users/{g.user.id}')
    return render_template('recipe.html')

@app.route('/api/recipes/<int:recipe_id>/edit/save_instructions', methods = ['POST'])
def save_instructions(recipe_id):
    selected_recipe = Recipe.query.get(recipe_id)
    if selected_recipe.instructions:
        selected_recipe.instructions = []
    instructions = list(request.json['instructions'])
    for instruction in instructions:
        if instruction != '':
            new_instruction = Instruction(text=instruction, recipe_id = recipe_id)
            selected_recipe.instructions.append(new_instruction)
    db.session.commit()
    return 'success'
#*******************************************************************************
#KrogerApi

""" @app.route('/api/get_access_token', methods = ['GET'])
def get_token():
    resp = requests.post('https://api.kroger.com/v1/connect/oauth2/token', 
                        data={"grant_type": "client_credentials", "scope": "product.compact" },
                        headers={"Content-Type": "application/x-www-form-urlencoded",
                                 "Authorization": "Basic aG9tZWNvb2stMWFmNWYzYWE1YmMwYTg2OGNiZWI3YTEwMGNjZWZlZDgyODQ1NzQ0MDEwNjM4MTEyODk5OnBSUVlWbHdtMENhdng0dUlBQWo0QUR4QUxXZ0llV0NYSkZLR3ZfN18="})
    token = resp.json()
    return token

@app.route('/api/ingredients/search/<string:keyword>/<string:token>')
def get_ingredients(keyword, token):
    print(keyword)
    print(token)
    resp = requests.get(f"https://api.kroger.com/v1/products?filter.term={keyword}", 
                        headers= {"Accept": "application/json",
                                  "Authorization": f"Bearer {token}"})
    results = resp.json()
    return results """