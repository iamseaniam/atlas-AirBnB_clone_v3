#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """This class manages storage of models in JSON format."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of all objects."""
        if cls is None:
            return self.__objects
        return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """Add a new object to the storage dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Save the objects to the JSON file."""
        with open(self.__file_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """Load objects from the JSON file."""
        try:
            with open(self.__file_path, "r") as f:
                data = json.load(f)
                for key, value in data.items():
                    cls_name, obj_id = key.split('.')
                    self.__objects[key] = eval(cls_name)(**value)
        except FileNotFoundError:
            pass

    def count(self, cls=None):
        """Count the number of objects of a given class."""
        if cls is None:
            return len(self.__objects)
        return len([obj for obj in self.__objects.values()
                    if isinstance(obj, cls)])

    def get(self, cls, id):
        """Retrieve an object by class and ID."""
        key = "{}.{}".format(cls.__name__, id)
        return self.__objects.get(key)
