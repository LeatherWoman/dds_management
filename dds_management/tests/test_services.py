from django.test import TestCase
from dds_management.services import TransactionService
from dds_management.models import Transaction, Status, TransactionType, Category, SubCategory
from datetime import date

class TransactionServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        cls.status = Status.objects.create(name="Бизнес")
        cls.transaction_type = TransactionType.objects.create(name="Пополнение")
        cls.category = Category.objects.create(
            name="Продажи", 
            transaction_type=cls.transaction_type
        )
        cls.subcategory = SubCategory.objects.create(
            name="Онлайн",
            category=cls.category
        )
        cls.transaction = Transaction.objects.create(
            date=date(2025, 1, 1),
            status=cls.status,
            transaction_type=cls.transaction_type,
            category=cls.category,
            subcategory=cls.subcategory,
            amount=1000
        )

    def test_filter_transactions(self):
        """Тест фильтрации транзакций по дате"""
        filtered = TransactionService.get_filtered_transactions(date_from='2025-01-01')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].id, self.transaction.id)