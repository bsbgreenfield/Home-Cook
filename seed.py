from app import app
from models import db, User, Cookbook, Recipe

db.drop_all()
db.create_all()


testuser = User.signup(username = 'test', password = 'test123', full_name= 'testuser', email='test@test.com', profile_pic=None)
db.session.add(testuser)
db.session.commit()
testcookbook = Cookbook(name='testcookbook', user_id = testuser.id)
cookbooktwo = Cookbook(name='cookbooktwo', user_id = testuser.id)
db.session.add(testcookbook)
db.session.add(cookbooktwo)
db.session.commit()
testrecipe = Recipe(name='testrecipe', rating = 10, user_id = testuser.id, cookbook_id = testcookbook.id)
testtwo = Recipe(name='testtwo', rating = 8, user_id = testuser.id, cookbook_id = testcookbook.id)
testthree = Recipe(name='testthree', rating = 6, user_id = testuser.id, cookbook_id = cookbooktwo.id)
testfour = Recipe(name='testfour', rating = 9, user_id = testuser.id, cookbook_id = cookbooktwo.id)
db.session.add_all([testrecipe, testtwo, testthree, testfour])
db.session.commit()

