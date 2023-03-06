from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    """login form"""

    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min=6)])

class SignUpForm(FlaskForm):
    """signup form"""

    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min=6)])
    full_name = StringField('Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    profile_pic = StringField('Profile Photo')

class AddCookbookForm(FlaskForm):
    """ADD a new cookbook"""

    name = StringField('Name', validators = [DataRequired()])
    recipes = SelectField('Recipes', validators=[Optional()])

class AddRecipeForm(FlaskForm):
    """Add a new recipe"""

    name = StringField('Name', validators = [DataRequired()])
    cookbook = SelectField('Add to a Cookbook',  validators=[Optional()] )

class BuildSearchForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])

class BuildTagForm(FlaskForm):
    tag = StringField('Tag', validators = [DataRequired()])

class BuildNotesForm(FlaskForm):
    note = StringField('Add Note', validators=[DataRequired()])

class BuildInstructionsForm(FlaskForm):
    instruction = StringField('Add Instruction', validators=[DataRequired()])

class RecipeQuickAdd(FlaskForm):
    recipe = SelectField()

class CustomIngredientForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired()])
    price = FloatField('Price: ', validators=[Optional()])

    
