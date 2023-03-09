import os
from flask import request, render_template, redirect, flash, Flask, session, g, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Cookbook, Recipe, Ingredient, Instruction, CustomIngredient, recipe_custom_ingredient, recipe_ingredient
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

@app.route('/recipes/build/edamam', methods= ['POST'])
def recipe_from_edamam():
    name = request.json['name']
    recipe_url = request.json['recipeUrl']
    recipe_cuisine = request.json['recipe_cuisine']
    ingredients = request.json['ingredients']
    new_recipe = Recipe(name=name, cookbook_id = None, user_id = g.user.id)
    db.session.add(new_recipe)
    db.session.commit()
    for ingredient in ingredients:
        print(ingredient)
        new_custom = CustomIngredient(name=ingredient['food'])
        new_recipe.child_custom_ingredients.append(new_custom)
        db.session.commit()

        # add in associated quantity and measure
        relational_table_row = recipe_custom_ingredient.query.filter(
            (recipe_custom_ingredient.recipe_custom_ingr == new_custom.id) &
              (recipe_custom_ingredient.ingredient_recipe == new_recipe.id)).first()
        relational_table_row.quantity = ingredient.get('quantity', None)
        relational_table_row.measure = ingredient.get('measure', None)
        db.session.add(relational_table_row)
        db.session.commit()
    return f'/recipes/{new_recipe.id}/edit'
    

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

@app.route('/api/recipes/<int:recipe_id>/edit/ingredient_info')
def send_ingredient_data(recipe_id):
    recipe_custom_rows = {f'c{row.recipe_custom_ingr}': (row.quantity, row.measure) for row in recipe_custom_ingredient.query.filter_by(ingredient_recipe=recipe_id).all()}
    recipe_standard_rows = {f's{row.recipe_ingredient}': (row.quantity, row.measure) for row in recipe_ingredient.query.filter_by(ingredient_recipe=recipe_id).all()}
    return jsonify(customData = recipe_custom_rows, standardData = recipe_standard_rows)

@app.route('/api/recipes/<int:recipe_id>/edit/<string:ingredient_name>/add', methods = ['POST'])
def add_ingredient_to_recipe(recipe_id, ingredient_name):
    recipe = Recipe.query.get_or_404(recipe_id)
    # check ingredientType
    if request.json['ingredient_type'] == 'standard-ingredient':
        ingredient = Ingredient.query.filter_by(name=ingredient_name).one()
        response = {'id': f's{ingredient.id}', 'name': ingredient.name}
        if ingredient:
            recipe.child_ingredients.append(ingredient)
            db.session.commit()
            return jsonify(response)
        return 'not ingredient'
    elif request.json['ingredient_type'] == 'custom-ingredient':
        # check if custom ingredient already exists
        existing_custom_ingredient = CustomIngredient.query.filter_by(name=ingredient_name).first()
        if existing_custom_ingredient:
            # if it already exists, check if it already exists in this recipe
            relational_table_row = recipe_custom_ingredient.query.filter(
                (recipe_custom_ingredient.recipe_custom_ingr == existing_custom_ingredient.id) &
                (recipe_custom_ingredient.ingredient_recipe == recipe_id)).first()
            if relational_table_row:
                return 'ingredient_already_exists!'
            else:
                recipe.child_custom_ingredients.append(existing_custom_ingredient)
                db.session.commit()
                response = {'id': f'c{existing_custom_ingredient.id}', 'name' : existing_custom_ingredient.name}
        else:
            custom_ingredient = CustomIngredient(name=ingredient_name)
            recipe.child_custom_ingredients.append(custom_ingredient)
            db.session.commit()
            response = {'id': f'c{existing_custom_ingredient.id}', 'name': custom_ingredient.name}
        return jsonify(response)
    else:
        return 'failed to add ingredient'

@app.route('/api/recipes/<int:recipe_id>/edit/updateIngredient', methods = ['POST'])
def update_ingredient(recipe_id):
    if request.json['type'] == 'custom-ingredient':
        relational_table_row = recipe_custom_ingredient.query.filter(
                (recipe_custom_ingredient.recipe_custom_ingr == request.json['id']) &
                (recipe_custom_ingredient.ingredient_recipe == recipe_id)).first()
        relational_table_row.quantity = request.json['quantity']
        relational_table_row.measure = request.json['measure']
        db.session.commit()
        responseId = f'c{request.json["id"]}'
    elif request.json['type'] == 'standard-ingredient':
        relational_table_row = recipe_ingredient.query.filter(
            (recipe_ingredient.recipe_ingredient == request.json['id']) &
            (recipe_ingredient.ingredient_recipe == recipe_id)).first()
        relational_table_row.quantity = request.json['quantity']
        relational_table_row.measure = request.json['measure']
        db.session.commit()
        responseId = f's{request.json["id"]}'
    else:
        return 'error, type not specified'
    response = {'id': responseId, 'quantity': relational_table_row.quantity, 'measure': relational_table_row.measure}
    return jsonify(response)
    
@app.route('/api/recipes/<int:recipe_id>/edit/delete', methods =['POST'])
def delete_ingredient(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.json['ingredient_type'] == 'standard':
        ingredient_id = request.json['ingredient_id']
        print(ingredient_id)
        ingredient = Ingredient.query.get(ingredient_id)
        recipe.child_ingredients.remove(ingredient)
        db.session.commit()
        return 'success'
    elif request.json['ingredient_type'] == 'custom':
        custom_ingredient_id = request.json['ingredient_id']
        selected_custom_ingredient = CustomIngredient.query.get(custom_ingredient_id)
        print(selected_custom_ingredient)
        recipe.child_custom_ingredients.remove(selected_custom_ingredient)
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