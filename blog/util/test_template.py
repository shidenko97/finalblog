import unittest

from blog import create_app, db
from config import TestConfig


class TestTemplate(unittest.TestCase):
    """Template for unit tests"""

    def setUp(self) -> None:
        """Setting up application for tests"""

        self.app = create_app()
        self.app.config.from_object(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        """Remove all settings for app after tests"""

        db.session.remove()
        db.drop_all()
        self.app_context.pop()
