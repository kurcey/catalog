import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# This class defines the coloums and relationships in the
# category table on the psql database
class Categories(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }


# This class defines the coloums and relationships in the
# user table on the psql database
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(256), index=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'username': self.username
        }


# This class defines the coloums and relationships in the
# item table on the psql database
class Item(Base):
    __tablename__ = 'item'

    title = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Categories)
    createdUser_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'cat_id': self.category_id,
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'created_User': self.user.username
        }


engine = create_engine('sqlite:///categories.db')

Base.metadata.create_all(engine)
