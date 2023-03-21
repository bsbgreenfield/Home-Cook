from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False, unique=True)
    full_name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String, nullable=False)
    profile_pic = db.Column(db.String, nullable=True, default= "/static/images/user-default.jpg")

    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )

    def is_followed_by(self, other_user):

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1

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
        db.session.commit()
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
    
    @classmethod
    def encrypt_new_password(cls, password):
        hashed_password = bcrypt.generate_password_hash(
            password).decode('UTF-8')
        return hashed_password

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
    url = db.Column(db.String, nullable = True)
    source = db.Column(db.String, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')
    cookbook_id = db.Column(db.Integer, db.ForeignKey('cookbooks.id', ondelete = "SET NULL"), nullable = True)
    cookbook = db.relationship(
        'Cookbook', backref='recipes')
    child_ingredients = db.relationship('Ingredient', secondary = 'recipes_ingredients', backref='recipes')
    instructions = db.relationship('Instruction', backref='recipe')
    notes = db.relationship('Note', backref='recipe')
    tags = db.relationship('Tag', secondary = 'recipes_tags', backref = 'attached_recipes')
    def serialize(self):
        ingredient_rows = [row.serialize_ingredient_row() for row
                            in recipe_ingredient.query.filter(recipe_ingredient.ingredient_recipe == self.id).all()]
        return {
            "id": self.id,
            "name": self.name,
            "rating":self.rating or 'unrated',
            'user_id':self.user_id,
            'ingredients': [{'id':ingredient_row['id'],
                            'ingredient_ident': ingredient_row['recipe_instance'],
                            'name': ingredient_row['name'],
                            'measure': ingredient_row['measure'],
                            'quantity': ingredient_row['quantity'], 
                            'prep': ingredient_row['prep']} 
                            for ingredient_row in ingredient_rows],
            'instructions': [{'id': instruction.id, 'text': instruction.text} for instruction in self.instructions],
            'url' : self.url
        }
class Tag(db.Model):

    __tablename__ = 'tags'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    recipes = db.relationship('Recipe', secondary = 'recipes_tags', backref = 'attached_tags')

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
        'recipes.id', ondelete='CASCADE'), nullable=True)
    



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



class recipe_ingredient(db.Model):

    __tablename__ = 'recipes_ingredients'

    recipe_ingredient = db.Column(
        db.Integer, db.ForeignKey('ingredients.id', ondelete="cascade"))
    ingredient_recipe = db.Column(
        db.Integer, db.ForeignKey('recipes.id', ondelete="cascade"))
    quantity = db.Column(db.String, nullable = True)
    measure = db.Column(db.String, nullable = True)
    prep = db.Column(db.String, nullable = True)
    recipe_instance = db.Column(db.String, nullable = False, primary_key=True)
    
    def serialize_ingredient_row(self):
        return{
            'id': self.recipe_ingredient,
            'recipe_instance': self.recipe_instance,
            'name': Ingredient.query.get(self.recipe_ingredient).name,
            'measure': self.measure,
            'quantity': self.quantity,
            'prep':self.prep
        }

