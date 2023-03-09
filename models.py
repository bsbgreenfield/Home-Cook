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
    child_custom_ingredients = db.relationship('CustomIngredient', secondary = 'recipes_custom_ingredients', backref= 'recipe' )
    instructions = db.relationship('Instruction', backref='recipe')
    notes = db.relationship('Note', backref='recipe')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rating":self.rating or 'unrated',
            'user_id':self.user_id,
            'ingredients': [{'id':ingredient.id, 'name': ingredient.name, 'price': ingredient.price} for ingredient in self.child_ingredients],
            'custom_ingredients': [{'id': custom_ingredient.id, 'name': custom_ingredient.name} for custom_ingredient in self.custom_ingredients],
            'instructions': [{'id': instruction.id, 'text': instruction.text} for instruction in self.instructions]
        }
class Tag(db.Model):

    __tablename__ = 'tags'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(30), nullable=False)

class recipe_tag(db.Model):

    __tablename__ = 'recipes_tags'

    tag_id = db.Column(
        db.Integer, db.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)
    recipe_id= db.Column(
        db.Integer, db.ForeignKey('recipes.id', ondelete="cascade"), primary_key=True)
    
    
class Instruction(db.Model):

    __tablename__ = 'instructions'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id', ondelete='CASCADE'), nullable=False)
    



class Note(db.Model):

    __tablename__ = 'notes'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete = 'CASCADE'), nullable = False)


class Ingredient(db.Model):

    __tablename__ =  'ingredients'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String, nullable = False)
    scientific_name = db.Column(db.String, nullable = True)
    group_cat = db.Column(db.String, nullable = True)
    sub_group = db.Column(db.String, nullable = True)
    price = db.Column(db.Float, nullable = True)

    parent_recipes = db.relationship('Recipe', secondary='recipes_ingredients', backref = 'ingredients')

class CustomIngredient(db.Model):
    
    __tablename__ = 'custom_ingredients'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String, nullable = False)
    parent_recipes = db.relationship('Recipe', secondary='recipes_custom_ingredients', backref = 'custom_ingredients')

class recipe_ingredient(db.Model):

    __tablename__ = 'recipes_ingredients'

    recipe_ingredient = db.Column(
        db.Integer, db.ForeignKey('ingredients.id', ondelete="cascade"), primary_key=True)
    ingredient_recipe = db.Column(
        db.Integer, db.ForeignKey('recipes.id', ondelete="cascade"), primary_key=True)
    quantity = db.Column(db.String, nullable = True)
    measure = db.Column(db.String, nullable = True)

class recipe_custom_ingredient(db.Model):

    __tablename__ = 'recipes_custom_ingredients'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    recipe_custom_ingr = db.Column(
        db.Integer, db.ForeignKey('custom_ingredients.id', ondelete="cascade"), nullable=False)
    ingredient_recipe = db.Column(
        db.Integer, db.ForeignKey('recipes.id', ondelete="cascade"), nullable=False)
    quantity = db.Column(db.String, nullable= True)
    measure = db.Column(db.String, nullable = True)
    price = db.Column(db.Integer, nullable = True)
