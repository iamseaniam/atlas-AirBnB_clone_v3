#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """This class manages storage of models in a database."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

    def all(self, cls=None):
        """Query all objects of a particular class."""
        objects = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(cls.__name__, obj.id)
                objects[key] = obj
        else:
            from models.base_model import BaseModel
            for cls in [State, City, User, Place, Amenity, Review]:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(cls.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add an object to the current database session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize session."""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def get(self, cls, id):
        """Retrieve an object by class and ID."""
        return self.__session.query(cls).get(id)

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class."""
        if cls:
            return self.__session.query(cls).count()
        else:
            count = 0
            for cls in [State, City, User, Place, Amenity, Review]:
                count += self.__session.query(cls).count()
        return count

    def close(self):
        """Call remove method on the private session attribute."""
        self.__session.close()
