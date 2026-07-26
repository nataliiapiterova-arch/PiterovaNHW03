import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import auth, database, models  # noqa: E402


class AuthTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._db_path = os.path.join(self._tmpdir.name, "test.db")
        self._orig_db_path = database.DB_PATH
        database.DB_PATH = self._db_path
        database._local.conn = None
        database.init_db()

    def tearDown(self):
        database.DB_PATH = self._orig_db_path
        database._local.conn = None
        self._tmpdir.cleanup()

    def test_password_hash_roundtrip(self):
        h, salt = auth.hash_password("correct horse battery staple")
        self.assertTrue(auth.verify_password("correct horse battery staple", h, salt))
        self.assertFalse(auth.verify_password("wrong password", h, salt))

    def test_signup_then_login(self):
        auth.signup("person@example.com", "supersecret1")
        user = auth.login("person@example.com", "supersecret1")
        self.assertEqual(user["email"], "person@example.com")
        self.assertEqual(user["plan"], "free")
        self.assertEqual(user["credits"], 1)

    def test_signup_duplicate_email_rejected(self):
        auth.signup("dupe@example.com", "supersecret1")
        with self.assertRaises(ValueError):
            auth.signup("dupe@example.com", "anotherpassword")

    def test_login_wrong_password_rejected(self):
        auth.signup("person2@example.com", "supersecret1")
        with self.assertRaises(ValueError):
            auth.login("person2@example.com", "wrongpassword")

    def test_session_token_roundtrip(self):
        user_id = auth.signup("tokens@example.com", "supersecret1")
        token = auth.create_session_token(user_id)
        user, csrf = auth.current_user_from_cookie(token)
        self.assertEqual(user["id"], user_id)
        self.assertIsNotNone(csrf)

    def test_invalid_token_returns_none(self):
        user, csrf = auth.current_user_from_cookie("not-a-real-token")
        self.assertIsNone(user)
        self.assertIsNone(csrf)

    def test_credit_gating(self):
        from app import billing

        user_id = auth.signup("credits@example.com", "supersecret1")
        user = models.get_user_by_id(user_id)
        self.assertTrue(billing.can_generate(user))
        billing.consume_credit(user)
        user = models.get_user_by_id(user_id)
        self.assertFalse(billing.can_generate(user))
        billing.upgrade_to_plan(user_id, "creator")
        user = models.get_user_by_id(user_id)
        self.assertTrue(billing.can_generate(user))
        self.assertEqual(user["plan"], "creator")
        self.assertEqual(user["credits"], billing.PLANS["creator"]["monthly_credits"])


if __name__ == "__main__":
    unittest.main()
