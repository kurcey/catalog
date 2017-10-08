from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Base, Item, User

engine = create_engine('sqlite:///categories.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create Categories
category1 = Categories(name="Soccer")
category2 = Categories(name="BasketBall")
category3 = Categories(name="BaseBall")
category4 = Categories(name="Frisbee")
category5 = Categories(name="SnowBoarding")
category6 = Categories(name="Rock Climbing")
category7 = Categories(name="FoosBall")
category8 = Categories(name="Skating")
category9 = Categories(name="Hockey")

# Add categories
session.add(category1)
session.add(category2)
session.add(category3)
session.add(category4)
session.add(category5)
session.add(category6)
session.add(category7)
session.add(category8)
session.add(category9)

# Create user
user1 = User(username="InitalSetup")

# Create Items
item1 = Item(title="Soccer Cleats",
             description="Type od shoes used when playing Soccer",
             category=category1, user=user1)
item2 = Item(title="Jersey",
             description="Shirt worn that identify Team and player",
             category=category1, user=user1)
item3 = Item(title="Shinguards",
             description="Protective gear used to protect shin   ",
             category=category1, user=user1)
item4 = Item(title="Two shinguards",
             description="two of type shinguards",
             category=category1, user=user1)
item5 = Item(title="Stick",
             description="Tools used to move ball around",
             category=category9, user=user1)
item6 = Item(title="Goggles",
             description="Protective eye wear",
             category=category5, user=user1)
item7 = Item(title="Snowboard",
             description="Used to move around in snow",
             category=category5, user=user1)
item8 = Item(title="Frisbee",
             description="Disk like object that is thrown around",
             category=category4, user=user1)
item9 = Item(title="Bat",
             description="Tool used in baseball to hit ball",
             category=category3, user=user1)

# Add items
session.add(item1)
session.add(item2)
session.add(item3)
session.add(item4)
session.add(item5)
session.add(item6)
session.add(item7)
session.add(item8)
session.add(item9)

# Commit the additions to the database
session.commit()
