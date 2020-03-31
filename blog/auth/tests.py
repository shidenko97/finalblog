from hashlib import md5
from time import sleep
import unittest

from sqlalchemy.exc import IntegrityError

from blog import db
from blog.auth.models import Role, User
from blog.util.test_template import TestTemplate


class UserModelCase(TestTemplate):
    """Unit tests for User model"""

    def test_avatar(self):
        """Test avatar loading"""

        user = User(email="test@test.test", fullname="Test Test")
        digest = md5(user.email.lower().encode("utf-8")).hexdigest()

        self.assertEqual(
            user.avatar(100),
            f"https://www.gravatar.com/avatar/{digest}?d=identicon&s=100"
        )

    def test_password(self):
        """Test password hashing"""

        user = User(password="test-user")
        user.hash_password()

        self.assertTrue(user.verify_pass("test-user"))
        self.assertFalse(user.verify_pass("not-test-user"))

    def test_restore_token(self):
        """Test password restoring token"""

        user = User(fullname="Test Test", email="test@test.test")
        db.session.add(user)
        db.session.commit()

        token = user.get_restore_token(2)

        self.assertEqual(user, user.verify_restore_token(token))

        sleep(3)

        # Check expired token
        self.assertIsNone(user.verify_restore_token(token))

    def test_email_unique(self):
        """Test email unique"""

        user = User(fullname="Test Test", email="test@test.test")
        db.session.add(user)
        db.session.commit()

        user_new = User(fullname="Test Test 1", email="test@test.test")
        db.session.add(user_new)

        # Check if DB throw exception on duplicate
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_roles(self):
        """Test adding and removing roles"""

        user = User(fullname="Test Test", email="test@test.test")

        role1 = Role(name="Role 1", description="Simple role 1")
        role2 = Role(name="Role 2", description="Simple role 2")

        # Add user role and check it
        user.roles.append(role1)
        self.assertIn(role1, user.roles)

        # Add user role and check it
        user.roles.append(role2)
        self.assertEqual([role1, role2], user.roles)

        # Remove user role and check it
        self.assertEqual(user.roles.pop(0), role1)

        # Check last role in user
        self.assertIn(role2, user.roles)


if __name__ == "__main__":
    unittest.main()
