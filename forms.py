from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional
from models import Tag

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
    profile_pic = StringField('Profile Photo (URL)')

class AddCookbookForm(FlaskForm):
    """ADD a new cookbook"""

    name = StringField('Name', validators = [DataRequired()])

class AddRecipeForm(FlaskForm):
    """Add a new recipe"""

    name = StringField('"New Recipe"', validators = [DataRequired()])
    cookbook = SelectField('Add to a Cookbook',  validators=[DataRequired()] )

class BuildSearchForm(FlaskForm):
    ingredient = StringField('Search', validators=[DataRequired()])

class BuildTagForm(FlaskForm):
    tag = SelectField('Tag', validators = [DataRequired()])

class BuildNotesForm(FlaskForm):
    note = StringField('Add Note', validators=[Optional()])

class BuildInstructionsForm(FlaskForm):
    instruction = StringField('Add Instruction', validators=[DataRequired()])

class RecipeQuickAdd(FlaskForm):
    recipe = SelectField()

class FriendSearchForm(FlaskForm):
    username = StringField('Search For a user', validators=[DataRequired()] )

class ChangeInfoForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    new_username = StringField('New Username (Optional)', validators=[Optional()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min=6)])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    full_name = StringField('Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    profile_pic = StringField('Profile Photo (URL)')

class addCommentForm(FlaskForm):
    text = TextAreaField('Comment: ', validators=[Length(min = 1)])
    
