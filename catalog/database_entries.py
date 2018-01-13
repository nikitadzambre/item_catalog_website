from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, CatalogItem

engine = create_engine('sqlite:///catalog.db')
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

# Add categories to database.
category = Category(name="Soccer")
session.add(category)
session.commit()

category = Category(name="Basketball")
session.add(category)
session.commit()

category = Category(name="Baseball")
session.add(category)
session.commit()

category = Category(name="Frisbee")
session.add(category)
session.commit()

category = Category(name="Snowboarding")
session.add(category)
session.commit()

category = Category(name="Rock Climbing")
session.add(category)
session.commit()

category = Category(name="Foosball")
session.add(category)
session.commit()

category = Category(name="Skating")
session.add(category)
session.commit()

category = Category(name="Hockey")
session.add(category)
session.commit()

print "Categories added to the Database."

# Add users to database.
user = User(name="Happy Me", email="happyme@gmail.com",
            picture="https://lh6.googleusercontent.com/-9uyq2wbdVds"
                    "/AAAAAAAAAAI/AAAAAAAAAzU/mqoVFU7zoIA/photo.jpg")
session.add(user)
session.commit()

user = User(name="Hello World", email="helloworld@gmail.com",
            picture="https://d125fmws0bore1.cloudfront.net/assets"
                    "/udacity_share-317a7f82552763598a5c91e1550b"
                    "7cd83663ce02d6d475d703e25a873cd3b574.png")
session.add(user)
session.commit()

user = User(name="Happy Me", email="happyme@gmail.com",
            picture="http://www.softsciencewebmedia.com/images/"
                    "WebTraining_Udacity.png")
session.add(user)
session.commit()

user = User(name="Happy Me", email="happyme@gmail.com",
            picture="http://www.appenics.com/wp-content/uploads/2015/01/"
                    "udacitycentre-367x367.jpg")
session.add(user)
session.commit()

print "Users added to the Database."

# Add items to database.
item = CatalogItem(title="Football", description="The ball used in the sport "
                   "of association football. The ball's spherical shape, "
                   "as well as its size, weight, and material composition, "
                   "are specified by Law 2 of the Laws of the Game maintained "
                   "by the International Football Association Board.",
                   category_name="Soccer", user_id=1)
session.add(item)
session.commit()

item = CatalogItem(title="Basketball", description="A basketball is a "
                   "spherical inflated ball used in basketball games. "
                   "Basketballs typically range in size from very small "
                   "promotional items only a few inches in diameter to extra "
                   "large balls nearly a foot in diameter used in training "
                   "exercises.", category_name="Basketball", user_id=2)
session.add(item)
session.commit()

item = CatalogItem(title="Baseball", description="A baseball is a ball used "
                   "in the sport of the same name, baseball. The ball features"
                   " a rubber or cork center, wrapped in yarn, and covered, "
                   "in the words of the Official Baseball Rules \"with two "
                   "strips of white horsehide or cowhide, tightly stitched "
                   "together.\"", category_name="Baseball", user_id=3)
session.add(item)
session.commit()

item = CatalogItem(title="Baseball Bat", description="A baseball bat is a "
                   "smooth wooden or metal club used in the sport of baseball "
                   "to hit the ball after it is thrown by the pitcher. By "
                   "regulation it may be no more than 2.75 inches (70 mm) "
                   "in diameter at the thickest part and no more than "
                   "42 inches (1,100 mm) long.", category_name="Baseball",
                   user_id=4)
session.add(item)
session.commit()

item = CatalogItem(title="Baseball Glove", description="A baseball glove or "
                   "mitt is a large leather glove worn by baseball players of "
                   "the defending team, which assists players in catching and "
                   "fielding balls hit by a batter or thrown by a teammate.",
                   category_name="Baseball", user_id=1)
session.add(item)
session.commit()

item = CatalogItem(title="Frisbee", description="A frisbee (also called a "
                   "flying disc or simply a disc) is a gliding toy or sporting"
                   " item that is generally plastic and roughly 20 to 25 "
                   "centimetres (8 to 10 in) in diameter with a lip, used "
                   "recreationally and competitively for throwing and catching"
                   ", for example, in flying disc games. The shape of the disc"
                   ", an airfoil in cross-section, allows it to fly by "
                   "generating lift as it moves through the air while "
                   "spinning.", category_name="Frisbee", user_id=2)
session.add(item)
session.commit()

item = CatalogItem(title="Boots", description="Snowboard boots are mostly "
                   "considered soft boots, though alpine snowboarding uses a "
                   "harder boot similar to a ski boot. A boot''s primary "
                   "function is to transfer the rider''s energy into the board"
                   ", protect the rider with support, and keep the rider''s "
                   "feet warm.", category_name="Snowboarding", user_id=3)
session.add(item)
session.commit()

item = CatalogItem(title="Snowboard", description="Snowboards are boards that "
                   "are usually the width of one''s foot longways, with the "
                   "ability to glide on snow.", category_name="Snowboarding",
                   user_id=4)
session.add(item)
session.commit()

item = CatalogItem(title="Climbing Ropes", description="Climbing ropes are "
                   "typically of kernmantle construction, consisting of a core"
                   " (kern) of long twisted fibres and an outer sheath "
                   "(mantle) of woven coloured fibres. The core provides "
                   "about 80% of the tensile strength, while the sheath is a "
                   "durable layer that protects the core and gives the rope "
                   "desirable handling characteristics.",
                   category_name="Rock Climbing", user_id=1)
session.add(item)
session.commit()

item = CatalogItem(title="Carabiner", description="Carabiners are metal loops "
                   "with spring-loaded gates (openings), used as connectors. "
                   "Once made primarily from steel, almost all carabiners for "
                   "recreational climbing are now made from a light weight "
                   "aluminum alloy.", category_name="Rock Climbing", user_id=2)
session.add(item)
session.commit()

item = CatalogItem(title="Quickdraw", description="Quickdraws (often referred "
                   "to as \"draws\") are used by climbers to connect ropes to "
                   "bolt anchors, or to other traditional protection, allowing"
                   " the rope to move through the anchoring system with "
                   "minimal friction.", category_name="Rock Climbing",
                   user_id=3)
session.add(item)
session.commit()

item = CatalogItem(title="Harness", description="A harness is a system used "
                   "for connecting the rope to the climber. There are two "
                   "loops at the front of the harness where the climber ties "
                   "into the rope at the working end using a figure-eight "
                   "knot.", category_name="Rock Climbing", user_id=4)
session.add(item)
session.commit()

item = CatalogItem(title="Roller Skates", description="Roller skates are shoes"
                   ", or bindings that fit onto shoes, that are worn to"
                   " enable the wearer to roll along on wheels.",
                   category_name="Skating", user_id=1)
session.add(item)
session.commit()

item = CatalogItem(title="Belay Device", description="Belay devices are"
                   " mechanical friction brake devices used to control a "
                   "rope when belaying. Their main purpose is to allow the "
                   "rope to be locked off with minimal effort to arrest a "
                   "climber''s fall. Multiple kinds of belay devices exist, "
                   "some of which may additionally be used as descenders for "
                   "controlled descent on a rope, as in abseiling or "
                   "rappelling.", category_name="Rock Climbing", user_id=4)
session.add(item)
session.commit()

print "Items added to database."
