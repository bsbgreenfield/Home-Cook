import os
from flask import request, render_template, redirect, flash, Flask, session, g, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Cookbook, Recipe, Ingredient, Instruction, recipe_ingredient, Tag
from forms import LoginForm, SignUpForm, AddCookbookForm, AddRecipeForm, BuildSearchForm, BuildTagForm, RecipeQuickAdd, FriendSearchForm, ChangeInfoForm

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
    """direct user to the welcome page if not logged in, else show homescreen"""
    if g.user:
        return redirect(f'/users/{g.user.id}')
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login user by runnning bcrypt authentication"""
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
    """sign up user with the signuo function and then log them in"""
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                full_name=form.full_name.data,
                profile_pic=form.profile_pic.data or None
            )
            db.session.commit()

        except IntegrityError:
            flash("Username is already taken!")
            return render_template('signup.html', form=form)
        first_cookbook = Cookbook(name='My First Cookbook', user_id = user.id)
        db.session.add(first_cookbook)
        db.session.commit()
        do_login(user)

        return redirect('/')

    return render_template('signup.html', form=form)


@app.route('/users/<int:user_id>')
def user_landing_page(user_id):
    """main landing page, only accessible by authenticated user"""
    if user_id == g.user.id:
        selected_user = User.query.get(user_id)
        recipe_count = 0
        cookbooks = selected_user.cookbooks
        for cookbook in cookbooks:
            recipe_count += len(cookbook.recipes)
        return render_template('main.html', cookbooks=cookbooks, recipe_count=recipe_count)
    else:
        return redirect(f'/users/{g.user.id}')


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user_profile(user_id):
    """allow logged in user to edit their own account. If new password or username, re-authenticate"""
    if user_id == g.user.id:
        form = ChangeInfoForm(obj=g.user)
        if form.validate_on_submit():
            user = User.authenticate(form.username.data, form.password.data)
            if user:
                if form.new_username.data:
                    user.username = form.new_username.data
                # if user chose a new password, encrypt it and set it as their new password
                if form.new_password.data:
                    user.password = User.encrypt_new_password(
                        form.new_password.data)
                user.full_name = form.full_name.data
                user.email = form.email.data
                user.profile_pic = form.profile_pic.data
                db.session.commit()
                return redirect('/')
            else:
                flash('Incorrect username or password')

        return render_template('edit_profile.html', user=g.user, form=form)
    else:
        return redirect(f'/users/{g.user.id}/profile')


@app.route('/users/<int:user_id>/friends', methods=['GET', 'POST'])
def friends_view(user_id):
    """view followers, following, and search from all users"""
    form = FriendSearchForm()
    if form.validate_on_submit():
        username_search_input = form.username.data
        user_results = User.query.filter(
            User.username.ilike(f'%{username_search_input}%')).all()
        if len(user_results) > 0:
            return render_template('friends.html', user_results=user_results, form=form)
        else:
            return render_template('friends.html', user_results='DNE', form=form)
    return render_template('friends.html', form=form, user_results=None)


@app.route('/recipes/build')
def recipe_from_scratch():
    """create a new recipe for the user to edit and add to their own cookbook"""
    new_recipe = Recipe(name='', cookbook_id=None, user_id=g.user.id)
    db.session.add(new_recipe)
    db.session.commit()
    return redirect(f'/recipes/{new_recipe.id}/edit')


@app.route('/recipes/build/edamam', methods=['POST'])
def recipe_from_edamam():
    """take json info from front end to create a new recipe"""
    name = request.json['name']
    recipe_url = request.json['recipeUrl']
    recipe_source = request.json['recipe_source']
    recipe_cuisine = request.json['recipe_cuisine']
    recipe_health_labels = request.json['health_labels']
    ingredients = request.json['ingredients']
    new_recipe = Recipe(name=name, cookbook_id=None,
                        user_id=g.user.id, url=recipe_url, source=recipe_source)
    db.session.add(new_recipe)
    db.session.commit()
    # add in tags to recipe
    recipe_cuisine.extend(recipe_health_labels)
    print(recipe_cuisine)
    for tag in recipe_cuisine:
        if tag:
            new_tag = Tag.query.filter_by(name=tag).first()
        if new_tag and new_tag not in new_recipe.tags:
            new_recipe.tags.append(new_tag)
    db.session.commit()
    for ingredient in ingredients:
        # if it already exists, check if its in the recipe already,
        #  create an appropriate unique ident either way
        existing_ingredient = Ingredient.query.filter(
            Ingredient.name.ilike(ingredient['food'])).first()
        if existing_ingredient:
            # check if there is already a row for the ingredient
            existing_recipe_ingredients = recipe_ingredient.query.filter(
                (recipe_ingredient.recipe_ingredient == existing_ingredient.id) &
                (recipe_ingredient.ingredient_recipe == new_recipe.id)).all()
            
            # set unique ingredient identifier based off of 
            # if there are other of the same ingredient in the receipe already
            if existing_recipe_ingredients:
                unique_ingredient_ident = f'{new_recipe.id}-{existing_ingredient.id}-{len(existing_recipe_ingredients) + 1}'
            else:
                unique_ingredient_ident = f'{new_recipe.id}-{existing_ingredient.id}-1'

            new_ingredient_instance = recipe_ingredient(recipe_ingredient=existing_ingredient.id,
                                                        ingredient_recipe=new_recipe.id,
                                                        recipe_instance=unique_ingredient_ident)
            db.session.add(new_ingredient_instance)
            db.session.commit()
            # get measure and quantity if provided, set it in the new ingredient row
            new_ingredient_instance.quantity = ingredient.get('quantity', None)
            if ingredient['measure'] == "<unit>":
                new_ingredient_instance.measure = None
            else:
                new_ingredient_instance.measure = ingredient.get('measure', None)
        else:
            new_custom = Ingredient(name=ingredient['food'])
            db.session.add(new_custom)
            db.session.commit()
            unique_ingredient_ident = f'{new_recipe.id}-{new_custom.id}-1'
            new_ingredient_instance = recipe_ingredient(recipe_ingredient=new_custom.id,
                                                        ingredient_recipe=new_recipe.id,
                                                        recipe_instance=unique_ingredient_ident)
            # get measure and quantity if provided, set it in the new ingredient row
            new_ingredient_instance.quantity = ingredient.get('quantity', None)
            if ingredient['measure'] == "<unit>":
                new_ingredient_instance.measure = None
            else:
                new_ingredient_instance.measure = ingredient.get('measure', None)
            # add in associated quantity and measure
            db.session.add(new_ingredient_instance)
            db.session.commit()
    return f'/recipes/{new_recipe.id}/edit'


@app.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def view_and_edit_recipe(recipe_id):
    """edit a recipe. Pull in any data about the recipe from database"""
    selected_recipe = Recipe.query.get(recipe_id)
    if selected_recipe.user_id == g.user.id:
        main_recipe_form = AddRecipeForm(
            name=selected_recipe.name, cookbook=selected_recipe.cookbook_id)
        main_recipe_form.cookbook.choices = [(cookbook.id, cookbook.name)
                                             for cookbook in Cookbook.query.filter_by(user_id=g.user.id)]
        build_search_form = BuildSearchForm()
        build_tag_form = BuildTagForm()
        available_tags = [tag for tag in Tag.query.all(
        ) if tag not in selected_recipe.tags]
        build_tag_form.tag.choices = [(tag.id, tag.name)
                                      for tag in available_tags]
        if build_tag_form.validate_on_submit():
            new_tag = Tag.query.filter_by(id=build_tag_form.tag.data).first()
            if new_tag:
                selected_recipe.tags.append(new_tag)
                print(new_tag)
                db.session.commit()
        return render_template('recipe.html', recipe=selected_recipe,
                               main_recipe_form=main_recipe_form,
                               build_search_form=build_search_form,
                               build_tag_form=build_tag_form)
    else:
        return redirect(f'/users/{g.user.id}')


@app.route('/users/<int:user_id>/cookbooks/add', methods=['GET', 'POST'])
def add_new_cookbook(user_id):
    """add a cookbok for logged in user"""
    if user_id == g.user.id:
        form = AddCookbookForm()
        if form.validate_on_submit():
            name = form.name.data
            new_cookbook = Cookbook(name=name, user_id=user_id)
            db.session.add(new_cookbook)
            db.session.commit()
            return redirect(f'/users/{user_id}')
        return render_template('add_cookbook.html', form=form)
    else:
        return redirect(f'/users/{g.user.id}')


@app.route('/cookbooks/<int:cookbook_id>/edit', methods=['GET', 'POST'])
def edit_cookbook(cookbook_id):
    """edit your own cookbooks"""
    selected_cookbook = Cookbook.query.get(cookbook_id)
    if selected_cookbook.user_id == g.user.id:
        form = AddCookbookForm(obj=selected_cookbook)
        if form.validate_on_submit():
            selected_cookbook.name = form.name.data
            db.session.commit()
            return redirect(f'/users/{g.user.id}')
        return render_template('edit_cookbook.html', form=form, cookbook=selected_cookbook)
    else:
        return redirect(f'/users/{g.user.id}')


@app.route('/users/<int:user_id>/profile')
def profile_view(user_id):
    """view any users profile and cookbooks"""
    selected_user = User.query.get(user_id)
    return render_template('profile.html', user=selected_user)


@app.route('/cookbooks/<int:cookbook_id>')
def view_cookbook(cookbook_id):
    """view any cookbook"""
    selected_cookbook = Cookbook.query.get(cookbook_id)
    return render_template('cookbook.html', cookbook=selected_cookbook)


# ******************************************************************************
# API routes

@app.route('/api/recipes/<int:recipe_id>/edit/info')
def send_recipe_data(recipe_id):
    """respond with json about the recipe being edited"""
    selected_recipe = Recipe.query.get(recipe_id)
    return jsonify(recipe=selected_recipe.serialize())


@app.route('/api/recipes/<int:recipe_id>/edit/ingredient_info')
def send_ingredient_data(recipe_id):
    """send ingredient data for each ingredient belonging to this recipe"""
    recipe_rows = {row.recipe_instance: row.serialize_ingredient_row() for row
                    in recipe_ingredient.query.filter_by(ingredient_recipe=recipe_id).all()}
    return jsonify(ingredientData=recipe_rows)


@app.route('/api/recipes/<int:recipe_id>/edit/<string:ingredient_name>/add', methods=['POST'])
def add_ingredient_to_recipe(recipe_id, ingredient_name):
    """add an ingredient to the recipe being edited
        use an existing ingredient if it exists"""
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id == g.user.id:
        # check if the ingredient already exists
        ingredient = Ingredient.query.filter(
            Ingredient.name.ilike(ingredient_name)).first()
        if ingredient:
            # if it exists, check if it is in this recipe
            existing_recipe_ingredients = recipe_ingredient.query.filter(
                (recipe_ingredient.recipe_ingredient == ingredient.id) &
                (recipe_ingredient.ingredient_recipe == recipe_id)).all()
            # if so create a new row in recipe_ingredient with a new unique identifier
            if existing_recipe_ingredients:
                unique_ingredient_ident = f'{recipe.id}-{ingredient.id}-{len(existing_recipe_ingredients) + 1}'
            else:
                unique_ingredient_ident = f'{recipe.id}-{ingredient.id}-1'
            new_ingredient_instance = recipe_ingredient(recipe_ingredient=ingredient.id,
                                                        ingredient_recipe=recipe.id,
                                                        recipe_instance=unique_ingredient_ident)
            db.session.add(new_ingredient_instance)
            db.session.commit()
            response = {'id': f'{ingredient.id}',
                        'name': ingredient.name,
                        'ingredient_ident': unique_ingredient_ident}
            return jsonify(response)
        # if ingredient doesnt already exist, create it and add it to recipe
        else:
            custom_ingredient = Ingredient(name=ingredient_name)
            db.session.add(custom_ingredient)
            db.session.commit()
            unique_ingredient_ident = f'{recipe.id}-{custom_ingredient.id}-1'
            new_ingredient_instance = recipe_ingredient(recipe_ingredient=custom_ingredient.id,
                                                        ingredient_recipe=recipe.id,
                                                        recipe_instance=unique_ingredient_ident)
            db.session.add(new_ingredient_instance)
            db.session.commit()
            response = {'id': f'{custom_ingredient.id}',
                        'name': custom_ingredient.name,
                        'ingredient_ident': unique_ingredient_ident}
            return jsonify(response)
    else:
        return 'not_authenticated'


@app.route('/api/recipes/<int:recipe_id>/edit/updateIngredient', methods=['POST'])
def update_ingredient(recipe_id):
    """find the appropriate row for the ingredient-recipe relational table and update measure and 
        quantity columns if appropriate"""
    selected_recipe = Recipe.query.get(recipe_id)
    if selected_recipe.user_id == g.user.id:
        relational_table_row = recipe_ingredient.query.get(request.json['ingredient_ident'])
        if relational_table_row:
            # set quantity info in relationsional table, repond with updated ingredient info
            relational_table_row.quantity = request.json['quantity']
            relational_table_row.measure = request.json['measure']
            db.session.commit()
            responseId = request.json['ingredient_ident']
        else:
            return 'ingredient_not_found'
        response = {'ingredient_ident': responseId, 'quantity': relational_table_row.quantity,
                    'measure': relational_table_row.measure}
        return jsonify(response)
    else:
        return 'not_authenticated'


@app.route('/api/recipes/<int:recipe_id>/edit/delete_ingredient', methods=['POST'])
def delete_ingredient(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id == g.user.id:
        ingredient_ident = request.json['ingredient_ident']
        ingredient_row = recipe_ingredient.query.filter_by(recipe_instance =ingredient_ident)
        if ingredient_row:
            ingredient_row.delete()
            db.session.commit()
            return 'success'
        else:
            return 'failure'
    else:
        return 'not_authenticated'


@app.route('/api/recipes/<int:recipe_id>/edit/delete_tag', methods=['POST'])
def delete_tag(recipe_id):
    selected_recipe = Recipe.query.get(recipe_id)
    if selected_recipe.user_id == g.user.id:
        tag_goner = Tag.query.get(request.json['tag_id'])
        selected_recipe.tags.remove(tag_goner)
        db.session.commit()
        if tag_goner not in selected_recipe.tags:
            return 'success'
        else:
            return 'failure'
    else:
        return 'not_authenticated'


@app.route('/api/recipes/<int:recipe_id>/edit/save', methods=['POST'])
def save_recipe(recipe_id):
    main_recipe_form = AddRecipeForm()
    main_recipe_form.cookbook.choices = [(cookbook.id, cookbook.name)
                                         for cookbook in Cookbook.query.filter_by(user_id=g.user.id)]
    selected_recipe = Recipe.query.get(recipe_id)
    if selected_recipe.user_id == g.user.id:
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
    else:
        return 'not_authenticated'


@app.route('/api/save_instructions', methods=['POST'])
def save_instructions():
    selected_recipe = Recipe.query.get(request.json['recipe_id'])
    if selected_recipe.instructions:
        for instruction in selected_recipe.instructions:
            Instruction.query.filter_by(id=instruction.id).delete()
            db.session.commit()
    instructions = list(request.json['instructions'])
    for instruction in instructions:
        if instruction != '':
            new_instruction = Instruction(
                text=instruction, recipe_id=selected_recipe.id)
            selected_recipe.instructions.append(new_instruction)
        db.session.commit()
    return 'success'


@app.route('/api/cookbooks/<int:cookbook_id>/remove_recipe/<int:recipe_id>', methods=['POST'])
def remove_recipe(cookbook_id, recipe_id):
    selected_cookbook = Cookbook.query.get(cookbook_id)
    if selected_cookbook.user_id == g.user.id:
        goner_recipe = Recipe.query.get(recipe_id)
        if goner_recipe in selected_cookbook.recipes:
            selected_cookbook.recipes.remove(goner_recipe)
            db.session.commit()
        return 'recipe-removed'
    else:
        return 'not_authenticated'


@app.route('/api/users/<int:curr_user_id>/friends/add/<int:new_follower_id>', methods=['POST'])
def add_friend(curr_user_id, new_follower_id):
    if g.user.id == curr_user_id:
        curr_user = User.query.get(curr_user_id)
        user_to_follow = User.query.get(new_follower_id)
        curr_user.following.append(user_to_follow)
        db.session.commit()
        return redirect(f'/users/{curr_user_id}/friends')
    else:
        return 'not_authenticated'


@app.route('/api/users/<int:curr_user_id>/friends/remove/<int:goner_follower_id>', methods=['POST'])
def remove_friend(curr_user_id, goner_follower_id):
    if g.user.id == curr_user_id:
        curr_user = User.query.get(curr_user_id)
        user_to_follow = User.query.get(goner_follower_id)
        curr_user.following.remove(user_to_follow)
        db.session.commit()
        return redirect(f'/users/{curr_user_id}/friends')
    else:
        return 'not_authenticated'


def create_recipe_copy(recipe_id):
    selected_recipe = Recipe.query.get(recipe_id)
    recipe_name = f'{selected_recipe.name}' + ' (copy)'
    recipe_url = selected_recipe.url
    recipe_source = selected_recipe.source
    recipe_user_id = g.user.id
    recipe_tags = selected_recipe.tags
    
    recipe_instructions = [Instruction(
        text=instruction.text) for instruction in selected_recipe.instructions]

    # create recipe and redirect to the edit screen
    copied_recipe = Recipe(name=recipe_name,
                           url=recipe_url,
                           source=recipe_source,
                           user_id=recipe_user_id,
                           tags=recipe_tags,
                           instructions=recipe_instructions)
    db.session.add(copied_recipe)
    db.session.commit()
    
    # create ingredient instances
    for ingredient_row in recipe_ingredient.query.filter_by(ingredient_recipe=selected_recipe.id).all():
        existing_recipe_ingredients = recipe_ingredient.query.filter(
                (recipe_ingredient.recipe_ingredient == ingredient_row.recipe_ingredient) &
                (recipe_ingredient.ingredient_recipe == copied_recipe.id)).all()
        # set unique ingredient identifier based off of 
        # if there are other of the same ingredient in the receipe already
        if existing_recipe_ingredients:
            unique_ingredient_ident = f'{copied_recipe.id}-{ingredient_row.recipe_ingredient}-{len(existing_recipe_ingredients) + 1}'
        else:
            unique_ingredient_ident = f'{copied_recipe.id}-{ingredient_row.recipe_ingredient}-1'
        new_ingredient_instance = recipe_ingredient(recipe_ingredient = ingredient_row.recipe_ingredient,
                                                    ingredient_recipe = copied_recipe.id,
                                                    quantity = ingredient_row.quantity,
                                                    measure = ingredient_row.measure,
                                                    recipe_instance = unique_ingredient_ident)
        db.session.add(new_ingredient_instance)
        db.session.commit()
    return copied_recipe


@app.route('/api/recipes/<int:recipe_id>/copy', methods=['POST'])
def copy_recipe(recipe_id):
    copied_recipe = create_recipe_copy(recipe_id)
    db.session.add(copied_recipe)
    db.session.commit()
    return redirect(f'/recipes/{copied_recipe.id}/edit')


@app.route('/api/cookbooks/<int:cookbook_id>/copy', methods=['POST'])
def copy_cookbook(cookbook_id):
    selected_cookbook = Cookbook.query.get(cookbook_id)
    cookbook_name = f'{selected_cookbook.name}' + '(copy)'
    cookbook_user_id = g.user.id
    cookbook_recipes = []
    for recipe in selected_cookbook.recipes:
        recipe_copy = create_recipe_copy(recipe.id)
        db.session.add(recipe_copy)
        db.session.commit()
        cookbook_recipes.append(recipe_copy)
    copied_cookbook = Cookbook(name=cookbook_name, user_id=cookbook_user_id)
    db.session.add(copied_cookbook)
    db.session.commit()
    copied_cookbook.recipes = cookbook_recipes
    db.session.commit()
    return redirect(f'/users/{g.user.id}')
