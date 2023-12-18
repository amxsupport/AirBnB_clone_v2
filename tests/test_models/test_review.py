#!/usr/bin/python3
"""Defines unnittests for models/review.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestReview(unittest.TestCase):
    """Unittests for testing the Review class."""

    @classmethod
    def setUpClass(cls):
        """Review testing setup.
        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage and Review instances for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.user = User(email="poppy@holberton.com", password="betty98")
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name="Betty")
        cls.review = Review(text="stellar", place_id=cls.place.id,
                            user_id=cls.user.id)

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """Review testing teardown.
        Restore original file.json.
        Delete the FileStorage, DBStorage and Review test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.state
        del cls.city
        del cls.user
        del cls.place
        del cls.review
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/review.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Review.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        us = Review(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "text"))
        self.assertTrue(hasattr(us, "place_id"))
        self.assertTrue(hasattr(us, "user_id"))


