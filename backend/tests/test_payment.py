from django.test import TestCase
from django.contrib.auth import get_user_model
from collect.models import Collect
from payment.models import Payment

User = get_user_model()


class TestPaymentModel(TestCase):
    def setUp(self):
        # Создаем фиктивного пользователя для всех тестов
        self.user = User.objects.create(username="testuser", password="testpass")

    def test_first_payment_increases_collected_and_donors(self):
        collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            collected_amount=0,
            donors_count=0,
            target_amount=1000
        )

        # Создаем первый платеж от этого же пользователя
        Payment.objects.create(
            collect=collect,
            user=self.user,
            amount=100
        )

        collect.refresh_from_db()
        self.assertEqual(collect.collected_amount, 100)
        self.assertEqual(collect.donors_count, 1)

    def test_second_payment_same_donor_increases_amount_only(self):
        collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            collected_amount=0,
            donors_count=0,
            target_amount=1000
        )

        Payment.objects.create(collect=collect, user=self.user, amount=100)
        Payment.objects.create(collect=collect, user=self.user, amount=50)

        collect.refresh_from_db()
        self.assertEqual(collect.collected_amount, 150)
        self.assertEqual(collect.donors_count, 1)  # не увеличивается

    def test_second_payment_different_donor_increases_donors_count(self):
        collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            collected_amount=0,
            donors_count=0,
            target_amount=1000
        )

        # Первый донор
        Payment.objects.create(collect=collect, user=self.user, amount=100)

        # Второй донор
        another_user = User.objects.create(username="anotheruser")
        Payment.objects.create(collect=collect, user=another_user, amount=50)

        collect.refresh_from_db()
        self.assertEqual(collect.collected_amount, 150)
        self.assertEqual(collect.donors_count, 2)

    def test_payment_without_donor_does_not_increase_donors_count(self):
        collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            collected_amount=0,
            donors_count=0,
            target_amount=1000
        )

        # Платеж без пользователя (если ваша модель Payment допускает user=None)
        Payment.objects.create(collect=collect, amount=50, user=None)

        collect.refresh_from_db()
        self.assertEqual(collect.collected_amount, 50)
        self.assertEqual(collect.donors_count, 0)