from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False, unique=True)
    full_name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String, nullable=False)
    profile_pic = db.Column(db.String, nullable=True)

    @classmethod
    def signup(cls, username, email, full_name, password, profile_pic):
        """sign up first time user
        Hashes password and creates user instance
        """

        hashed_password = bcrypt.generate_password_hash(
            password).decode('UTF-8')

        created_user = User(username=username, email=email, full_name=full_name,
                            password=hashed_password, profile_pic=profile_pic)
        
        db.session.add(created_user)
        return created_user

    @classmethod
    def authenticate(cls, username, password):
        """find user in databse that matches the given username and password
        return that user if found
        otherwise return false"""

        user = User.query.filter_by(username=username).first()
        if user:
            is_authenticated = bcrypt.check_password_hash(
                user.password, password)
            if is_authenticated:
                return user
            else:
                return False
        return False


class Cookbook(db.Model):
    """cookbook class
    cookbook -> user"""

    __tablename__ = 'cookbooks'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', backref = 'cookbooks')



class Recipe(db.Model):

    __tablename__ = 'recipes'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User')
    cookbook_id = db.Column(db.Integer, db.ForeignKey('cookbooks.id', ondelete = "SET NULL"), nullable = True)
    cookbook = db.relationship(
        'Cookbook', backref='recipes')
    
    child_ingredients = db.relationship('Ingredient', secondary = 'recipes_ingredients', backref='recipes')
    instructions = db.relationship('Instruction', backref='recipe')



class Instruction(db.Model):

    __tablename__ = 'instructions'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    recipe = db.Column(db.Integer, db.ForeignKey(
        'recipes.id', ondelete='CASCADE'), nullable=False)
    

class Ingredient(db.Model):

    __tablename__ =  'ingredients'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(55), nullable = False)
    price = db.Column(db.Float, nullable = True)

    parent_recipes = db.relationship('Recipe', secondary='recipes_ingredients', backref = 'ingredients')

class recipe_ingredient(db.Model):

    __tablename__ = 'recipes_ingredients'

    recipe_ingredient = db.Column(
        db.Integer, db.ForeignKey('ingredients.id', ondelete="SET NULL"), primary_key=True)
    ingredient_recipe = db.Column(
        db.Integer, db.ForeignKey('recipes.id', ondelete="cascade"), primary_key=True)
    
