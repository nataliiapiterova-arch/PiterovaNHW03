import hashlib
import hmac
import json
import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import billing, database, models, stripe_client  # noqa: E402

WEBHOOK_SECRET = "whsec_test_secret"


def _sign(payload_bytes, secret=WEBHOOK_SECRET, timestamp=None):
    timestamp = timestamp if timestamp is not None else int(time.time())
    signed_payload = f"{timestamp}.".encode("utf-8") + payload_bytes
    signature = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={signature}"


class StripeSignatureTests(unittest.TestCase):
    def test_valid_signature_verifies(self):
        payload = b'{"type": "checkout.session.completed"}'
        header = _sign(payload)
        self.assertTrue(stripe_client.verify_webhook_signature(payload, header, WEBHOOK_SECRET))

    def test_tampered_payload_fails(self):
        payload = b'{"type": "checkout.session.completed"}'
        header = _sign(payload)
        self.assertFalse(
            stripe_client.verify_webhook_signature(b'{"type": "evil"}', header, WEBHOOK_SECRET)
        )

    def test_wrong_secret_fails(self):
        payload = b'{"type": "checkout.session.completed"}'
        header = _sign(payload)
        self.assertFalse(stripe_client.verify_webhook_signature(payload, header, "wrong_secret"))

    def test_expired_timestamp_fails(self):
        payload = b'{"type": "checkout.session.completed"}'
        header = _sign(payload, timestamp=int(time.time()) - 10_000)
        self.assertFalse(stripe_client.verify_webhook_signature(payload, header, WEBHOOK_SECRET))

    def test_missing_header_fails(self):
        self.assertFalse(stripe_client.verify_webhook_signature(b"{}", None, WEBHOOK_SECRET))

    def test_malformed_header_fails(self):
        self.assertFalse(
            stripe_client.verify_webhook_signature(b"{}", "not-a-valid-header", WEBHOOK_SECRET)
        )


class BillingTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._orig_db_path = database.DB_PATH
        database.DB_PATH = os.path.join(self._tmpdir.name, "test.db")
        database._local.conn = None
        database.init_db()
        for var in ("STRIPE_SECRET_KEY", "STRIPE_PRICE_ID", "STRIPE_WEBHOOK_SECRET"):
            os.environ.pop(var, None)

    def tearDown(self):
        database.DB_PATH = self._orig_db_path
        database._local.conn = None
        self._tmpdir.cleanup()
        for var in ("STRIPE_SECRET_KEY", "STRIPE_PRICE_ID", "STRIPE_WEBHOOK_SECRET"):
            os.environ.pop(var, None)

    def test_stripe_disabled_by_default(self):
        self.assertFalse(billing.stripe_enabled())

    def test_stripe_enabled_requires_secret_key(self):
        os.environ["STRIPE_SECRET_KEY"] = "sk_test_x"
        self.assertTrue(billing.stripe_enabled())

    def test_start_upgrade_falls_back_without_stripe_config(self):
        user_id = models.create_user("demo@example.com", "hash", "salt")
        user = models.get_user_by_id(user_id)
        target = billing.start_upgrade(
            user, "creator", "https://example.com/success", "https://example.com/cancel"
        )
        self.assertEqual(target, "https://example.com/success")
        updated = models.get_user_by_id(user_id)
        self.assertEqual(updated["plan"], "creator")
        self.assertEqual(updated["credits"], billing.PLANS["creator"]["monthly_credits"])

    def test_start_upgrade_rejects_non_purchasable_plan(self):
        user_id = models.create_user("badplan@example.com", "hash", "salt")
        user = models.get_user_by_id(user_id)
        with self.assertRaises(ValueError):
            billing.start_upgrade(user, "free", "https://example.com/success", "https://example.com/cancel")

    def test_process_webhook_upgrades_user_to_plan_from_metadata(self):
        os.environ["STRIPE_WEBHOOK_SECRET"] = WEBHOOK_SECRET
        user_id = models.create_user("webhook@example.com", "hash", "salt")
        payload = json.dumps({
            "type": "checkout.session.completed",
            "data": {"object": {
                "client_reference_id": str(user_id),
                "metadata": {"plan": "publisher"},
            }},
        }).encode("utf-8")
        header = _sign(payload)

        result = billing.process_webhook(payload, header)

        self.assertTrue(result)
        updated = models.get_user_by_id(user_id)
        self.assertEqual(updated["plan"], "publisher")
        self.assertEqual(updated["credits"], billing.PLANS["publisher"]["monthly_credits"])

    def test_process_webhook_rejects_bad_signature(self):
        os.environ["STRIPE_WEBHOOK_SECRET"] = WEBHOOK_SECRET
        user_id = models.create_user("badsig@example.com", "hash", "salt")
        payload = json.dumps({
            "type": "checkout.session.completed",
            "data": {"object": {
                "client_reference_id": str(user_id),
                "metadata": {"plan": "creator"},
            }},
        }).encode("utf-8")

        result = billing.process_webhook(payload, "t=1,v1=deadbeef")

        self.assertFalse(result)
        self.assertEqual(models.get_user_by_id(user_id)["plan"], "free")

    def test_process_webhook_without_secret_configured_returns_false(self):
        payload = b'{"type": "checkout.session.completed"}'
        self.assertFalse(billing.process_webhook(payload, _sign(payload)))

    def test_ensure_credits_fresh_leaves_free_plan_alone(self):
        user_id = models.create_user("free@example.com", "hash", "salt")
        user = models.get_user_by_id(user_id)
        refreshed = billing.ensure_credits_fresh(user)
        self.assertEqual(refreshed["credits"], 1)

    def test_ensure_credits_fresh_resets_paid_plan_after_reset_date(self):
        import datetime as dt

        user_id = models.create_user("paid@example.com", "hash", "salt")
        billing.upgrade_to_plan(user_id, "creator")
        models.decrement_credit(user_id)
        models.decrement_credit(user_id)
        past = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).isoformat()
        models.set_user_credits(user_id, 0, past)

        refreshed = billing.ensure_credits_fresh(models.get_user_by_id(user_id))

        self.assertEqual(refreshed["credits"], billing.PLANS["creator"]["monthly_credits"])


if __name__ == "__main__":
    unittest.main()
