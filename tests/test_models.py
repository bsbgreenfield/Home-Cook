import os
from unittest import TestCase
from models import db, User, Cookbook, Recipe, Ingredient

os.environ['DATABASE_URL'] = "postgresql:///cook_test"

from app import app

db.create_all()

class ModelTestCase(TestCase):
    """Test user model functionality"""
    
    def setUp(self):
        User.query.delete()
        Cookbook.query.delete()
        Recipe.query.delete()
        Ingredient.query.delete()
        self.client = app.test_client()
        self.testuser = User.signup(username='testuser',
                         password='hashed',
                           email='test@test.com', 
                           full_name='testuser',
                           profile_pic=None)
        db.session.add(self.testuser)
        db.session.commit()

    def test_signup_and_authenticate(self):
        # test signup
        u = User.signup(username='test',
                         password='hashedtest',
                           email='test@test.com', 
                           full_name='test',
                           profile_pic=None)
        db.session.add(u)
        db.session.commit()
        self.assertIsInstance(u, User)

        # test invalide signup
        with self.assertRaises(TypeError):
            User.signup(username='test2')

        # test authentication
        self.assertIsInstance(u.authenticate('test', 'hashedtest'), User )

        # test invalid authentication
        self.assertNotIsInstance(u.authenticate('xxxxxx', 'xxxxxx'), User)

    def test_cookbooks_and_recipes(self):
        cookbook = Cookbook(name='testcookbook', user_id = self.testuser.id)
        recipe = Recipe(name='testrecipe', rating = 10, user_id = self.testuser.id)

        db.session.add_all([cookbook, recipe])
        db.session.commit()

        # test cookbook and recipe, cookbook should have no recipes
        self.assertIsInstance(cookbook, Cookbook)
        self.assertEqual(recipe.rating, 10)
        self.assertEqual(len(cookbook.child_recipes), 0)

        # add recipe to cookbook
        cookbook.child_recipes.append(recipe)
        db.session.commit()

        # test that the cookbook has associted user, and is within user.cookbooks
        self.assertEqual(len(self.testuser.cookbooks), 1)
        self.assertIn(cookbook, self.testuser.cookbooks)

        # test that recipe has associated cookbook and is within cookbook.childrecipes
        self.assertEqual(len(cookbook.child_recipes), 1)
        self.assertIsInstance(cookbook.child_recipes[0], Recipe)
        self.assertIn(recipe, cookbook.child_recipes)

    def test_add_ingredients(self):
        cookbook = Cookbook(name='testcookbook', user_id = self.testuser.id)
        recipe = Recipe(name='testrecipe', rating = 10, user_id = self.testuser.id)

        db.session.add_all([cookbook, recipe])
        db.session.commit()