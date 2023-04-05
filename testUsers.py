from models import User, connect_db
from random import choice
from app import app

app.app_context().push()

names = ['Jake', 'Ezequiel', 'Prince', 'Aziel', 'Cristian', 'Raymond', 'Kane', 'Anderson', 'Odin', 'Chance', 'Wade', 'Gunner', 'Cairo', 'Colson', 'Ellis', 'Manuel', 'Julius', 'Jaylen', 'Erick', 'Angelo', 'Spencer', 'Orion', 'Bradley', 'Cody', 'Dante', 'Gideon', 'Josue', 'Joaquin', 'Jaden', 'Muhammad', 'Tate', 'Karson', 'Jensen', 'Martin', 'Derek', 'Daxton', 'Reid', 'Kobe', 'Cruz', 'Francisco', 'Rory', 'Khalil', 'Zander', 'Maximiliano', 'Niko', 'Andre', 'Cayden', 'Brian', 'Cohen', 'Aidan', 'Bryan', 'Bodhi', 'Kayson', 'Malcolm', 'Zayn', 'Damien', 'Emerson', 'Clayton', 'Tobias', 'Jorge', 'Hendrix', 'Ronan', 'Callum', 'Brady', 'Walter', 'Dallas', 'Colin', 'Brantley', 'Crew', 'Atticus', 'Finley', 'Omar', 'Maximus', 'Kairo', 'Lane', 'Kaden', 'Nico', 'Kenneth', 'Paul', 'Malakai', 'Paxton', 'Lennox', 'Cash', 'Mark', 'Louis', 'Bryce', 'Javier', 'Phoenix', 'Simon', 'Riley', 'Kaleb', 'Jett', 'Jax', 'Kyler', 'Preston', 'Kash', 'Jeremy', 'Zane', 'Rafael', 'Holden', 'Steven', 'Israel', 'Nash', 'Griffin', 'Remington', 'Caden', 'Hayes', 'Marcus', 'Lukas', 'Oscar', 'Matias', 'Kyrie', 'Adonis', 'Beckham', 'Knox', 'Colt', 'Emilio', 'Andres', 'Edward', 'Richard', 'Peter', 'Patrick', 'Eric', 'Grant', 'Joel', 'Avery', 'Victor', 'Tristan', 'Dawson', 'Alejandro', 'Blake', 'Zayden', 'Jesse', 'Abraham', 'Timothy', 'Karter', 'Amari', 'Beckett', 'Alan', 'Abel', 'Miguel', 'Alex', 'Felix', 'Barrett', 'Emmanuel', 'Arlo', 'Charlie', 'Nicolas', 'Xander', 'Brody', 'King', 'Finn', 'Judah', 'Kevin', 'Brandon', 'Tucker', 'Justin', 'Antonio', 'Leon', 'Hayden', 'Camden', 'Maddox', 'Gavin', 'Messiah', 'Emiliano', 'Jesus', 'Elliott', 'Ivan',
         'Malachi', 'Matteo', 'Dean', 'Juan', 'Maxwell', 'Kaiden', 'Graham', 'Elliot', 'Max', 'Jayce', 'Tyler', 'Ace', 'Arthur', 'Adriel', 'Ryker', 'Carlos', 'Bentley', 'Jude', 'Atlas', 'Rhett', 'Ashton', 'Braxton', 'Calvin', 'Zachary', 'Ayden', 'Theo', 'Thiago', 'Jonah', 'Enzo', 'Archer', 'Luis', 'Zion', 'Lorenzo', 'George', 'Nathaniel', 'Cole', 'Brayden', 'Jason', 'Walker', 'Jasper', 'Milo', 'Diego', 'Chase', 'Giovanni', 'Amir', 'Bryson', 'August', 'Harrison', 'Myles', 'Legend', 'Vincent', 'Evan', 'Luka', 'Sawyer', 'Damian', 'Kingston', 'Ryder', 'River', 'Gael', 'Kayden', 'Micah', 'Rowan', 'Declan', 'Adam', 'Emmett', 'Jace', 'Jaxson', 'Xavier', 'Dominic', 'Carson', 'Connor', 'Austin', 'Weston', 'Beau', 'Parker', 'Nicholas', 'Silas', 'Bennett', 'Jose', 'Jordan', 'Leonardo', 'Hunter', 'Jeremiah', 'Wesley', 'Greyson', 'Everett', 'Ian', 'Jameson', 'Robert', 'Jonathan', 'Brooks', 'Axel', 'Roman', 'Colton', 'Landon', 'Christian', 'Kai', 'Easton', 'Waylon', 'Cooper', 'Angel', 'Ryan', 'Aaron', 'Eli', 'Santiago', 'Cameron', 'Adrian', 'Nolan', 'Nathan', 'Joshua', 'Andrew', 'Isaiah', 'Jaxon', 'Miles', 'Ezekiel', 'Christopher', 'Caleb', 'Charles', 'Josiah', 'Elias', 'Maverick', 'Thomas', 'Lincoln', 'Dylan', 'Anthony', 'Luca', 'Jayden', 'Isaac', 'Carter', 'Gabriel', 'Ezra', 'Matthew', 'Grayson', 'Hudson', 'Julian', 'Luke', 'Leo', 'David', 'Wyatt', 'Joseph', 'John', 'Aiden', 'Asher', 'Jacob', 'Samuel', 'Owen', 'Logan', 'Ethan', 'Sebastian', 'Mason', 'Michael', 'Daniel', 'Mateo', 'Jackson', 'Alexander', 'Levi', 'Jack', 'Theodore', 'Henry', 'Lucas', 'Benjamin', 'William', 'James', 'Elijah', 'Oliver', 'Noah', 'Liam']

for num in range(100):
    choice1 = choice(names)
    choice2 = choice(names)
    User.signup(username = f'{choice1}{choice2}', password = choice(names),
                 full_name =  f'{choice1} {choice2}', email = f'{choice1}.{choice2}@gmail.com', 
                 profile_pic= None)
