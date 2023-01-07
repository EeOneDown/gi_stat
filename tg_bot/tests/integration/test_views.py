from unittest.mock import patch, Mock

from django.contrib.auth.models import User as DjangoUser
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(BASE_DOMAIN="test.com")
@override_settings(TELEGRAM_BOT_SECRET_TOKEN="test-secret-token")
@patch("telebot.TeleBot.set_webhook")
class SetWebhookTestCase(TestCase):
    def setUp(self) -> None:
        self.admin_user = DjangoUser.objects.create(username="test-admin", email="test@test.com", is_staff=True)
        self.admin_user.set_password("test-password")
        self.admin_user.save()

    def test_bot_called(self, mocked_set_webhook: Mock):
        self.assertTrue(self.client.login(username=self.admin_user.username, password="test-password"))
        response = self.client.get(reverse("set_webhook"))
        self.assertEqual(response.status_code, 200)
        mocked_set_webhook.assert_called_once()
        called_args, called_kwargs = mocked_set_webhook.call_args
        self.assertTupleEqual(called_args, ())
        self.assertEqual(called_kwargs["url"], "https://test.com/tg_bot/webhook")
        self.assertEqual(called_kwargs["secret_token"], "test-secret-token")

    def test_login_required(self, mocked_set_webhook: Mock):
        response = self.client.get(reverse("set_webhook"))
        self.assertEqual(response.status_code, 302)
        mocked_set_webhook.assert_not_called()
