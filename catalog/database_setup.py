from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):

    """The User class defines the attributes of a user
       who logs in to the application. This class also corresponds to the
       table 'user' in the database.
    Attributes:
        id (int): Unique ID generated for that user.
        name (str): Name of the user.
        email (str): Email address of the user.
        picture (str): URL of the photo of the user.
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(30))
    picture = Column(String(250))


class Category(Base):

    """The Category class defines the attributes of a category. This class
       also corresponds to the table 'category' in the database.
    Attributes:
        name (str): Unique name of that category.
    """

    __tablename__ = 'category'

    name = Column(String(250), primary_key=True)

    @property
    def serialize(self):

        '''Helps to send JSON objects in a serializable format'''

        return {
            'category_name': self.name,
        }


class CatalogItem(Base):

    """The CatalogItem class defines the attributes of a catalog item. This
       class also corresponds to the table 'catalog_item' in the database.
    Attributes:
        title (str): Unique name of that item.
        description (str): Description of the item.
        created_date (str): Date and time when he item was created.
        category_name (str): Name of the category which this item falls into.
        user_id (str): ID of the user who created this item.
    """

    __tablename__ = 'catalog_item'

    title = Column(String(80), primary_key=True)
    description = Column(String(250))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    category_name = Column(Integer, ForeignKey('category.name'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        '''Helps to send JSON objects in a serializable format'''

        return {
            'title': self.title,
            'description': self.description,
            'created_date': self.created_date,
        }

engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
