import os
from flask import request, render_template, redirect, flash, Flask, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Cookbook, Recipe, Ingredient, Instruction
from forms import LoginForm, SignUpForm, AddCookbookForm, AddRecipeForm, BuildSearchForm, BuildTagForm, BuildNotesForm, BuildInstructionsForm, RecipeQuickAdd

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
    form = RecipeQuickAdd()
    form.recipe.choices = [(recipe.id, recipe.name)
                             for recipe in Recipe.query.all()]
    selected_user = User.query.get(user_id)
    cookbooks = selected_user.cookbooks
    return render_template('main.html', cookbooks=cookbooks, form=form)

@app.route('/recipes/build')
def recipe_from_scratch():
    new_recipe = Recipe(name='New Recipe', cookbook_id = None, user_id=g.user.id)
    db.session.add(new_recipe)
    db.session.commit()     # figure out a way to not have to commit if recipe is cancelled?
    return redirect(f'/recipes/{new_recipe.id}/edit')

@app.route('/recipes/<int:recipe_id>/edit', methods = ['GET', 'POST'])
def view_and_edit_recipe(recipe_id):
    selected_recipe = Recipe.query.get(recipe_id)
    main_recipe_form = AddRecipeForm(name=selected_recipe.name, cookbook=selected_recipe.cookbook_id)
    main_recipe_form.cookbook.choices = [(cookbook.id, cookbook.name)
                             for cookbook in Cookbook.query.filter_by(user_id=g.user.id)]
    build_search_form = BuildSearchForm()
    build_tag_form = BuildTagForm()
    build_notes_form = BuildNotesForm()
    build_instructions_form = BuildInstructionsForm()
    if main_recipe_form.validate_on_submit():
        name = main_recipe_form.name.data
        cookbook_id = main_recipe_form.cookbook.data
        selected_recipe.name = name
        selected_recipe.cookbook_id = cookbook_id
        db.session.add(selected_recipe)
        db.session.commit()
        return redirect(f'/users/{g.user.id}')
    return render_template('recipe.html', recipe=selected_recipe,
                            main_recipe_form=main_recipe_form,
                              build_search_form=build_search_form,
                                build_tag_form=build_tag_form,
                                  build_notes_form=build_notes_form,
                                    build_instructions_form=build_instructions_form)



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
    if Recipe.query.all():
        form.recipes.choices = [(recipe.id, recipe.name)
                                for recipe in Recipe.query.all()]
    else:
        form.recipes.choices = ['No Recipes Found']
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