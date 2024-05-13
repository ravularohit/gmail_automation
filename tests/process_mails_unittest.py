import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from src.models import Email
from src.process_mails import apply_rule, perform_action

class TestEmailProcessing(unittest.TestCase):

    def test_apply_rule_contains(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        rule = {"field": "subject", "predicate": "contains", "value": "Test"}
        self.assertTrue(apply_rule(rule, email))

    def test_apply_rule_notcontains(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        rule = {"field": "subject", "predicate": "notcontains", "value": "Hello"}
        self.assertTrue(apply_rule(rule, email))

    def test_apply_rule_eq(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        rule = {"field": "subject", "predicate": "eq", "value": "Test Subject"}
        self.assertTrue(apply_rule(rule, email))

    def test_apply_rule_neq(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        rule = {"field": "subject", "predicate": "neq", "value": "Another Subject"}
        self.assertTrue(apply_rule(rule, email))

    def test_apply_rule_date_received_lt(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        rule = {"field": "date_received", "predicate": "lt", "value": "1"}
        self.assertTrue(apply_rule(rule, email))

    def test_apply_rule_date_received_gt(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        rule = {"field": "date_received", "predicate": "gt", "value": "1"}
        self.assertFalse(apply_rule(rule, email))

    def test_perform_action_mark_as_read(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        service_mock = MagicMock()
        perform_action({"type": "mark as read"}, email, service_mock)
        service_mock.users().messages().modify.assert_called_once_with(userId='me', id="test_id", body={'removeLabelIds': ['UNREAD']})

    def test_perform_action_mark_as_unread(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        service_mock = MagicMock()
        perform_action({"type": "mark as unread"}, email, service_mock)
        service_mock.users().messages().modify.assert_called_once_with(userId='me', id="test_id", body={'addLabelIds': ['UNREAD']})
    def test_perform_action_move_message(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        service_mock = MagicMock()
        service_mock.users().labels().list().execute.return_value = {"labels": [{"name": "label1", "id": "label1_id"}]}
        perform_action({"type": "move message", "value": "label1"}, email, service_mock)
        service_mock.users().messages().modify.assert_called_once_with(userId='me', id="test_id", body={'addLabelIds': ['label1']})

    def test_perform_action_move_message_label_not_found(self):
        email = Email(id="test_id",sender="test@example.com",subject="Test Subject",labels="important",date_received="Wed, 01 Jan 2023 12:00:00 +0000")
        service_mock = MagicMock()
        service_mock.users().labels().list().execute.return_value = {"labels": []}
        perform_action({"type": "move message", "value": "nonexistent_label"}, email, service_mock)
        service_mock.users().messages().modify().assert_not_called()

