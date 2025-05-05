from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from dds_management.models import (
    Status,
    TransactionType,
    Category,
    SubCategory,
    Transaction
)

class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        cls.status = Status.objects.create(name="Бизнес")
        cls.income_type = TransactionType.objects.create(name="Пополнение")
        cls.expense_type = TransactionType.objects.create(name="Списание")
        
        cls.income_category = Category.objects.create(
            name="Продажи",
            transaction_type=cls.income_type
        )
        cls.expense_category = Category.objects.create(
            name="Маркетинг",
            transaction_type=cls.expense_type
        )
        
        cls.income_subcategory = SubCategory.objects.create(
            name="Онлайн",
            category=cls.income_category
        )
        cls.expense_subcategory = SubCategory.objects.create(
            name="Реклама",
            category=cls.expense_category
        )

    def test_transaction_creation(self):
        """Тест создания транзакции"""
        transaction = Transaction.objects.create(
            date=date(2025, 1, 1),
            status=self.status,
            transaction_type=self.income_type,
            category=self.income_category,
            subcategory=self.income_subcategory,
            amount=1000
        )
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.transaction_type, self.income_type)

    def test_invalid_category_type_validation(self):
        """Тест валидации несоответствия категории и типа"""
        transaction = Transaction(
            date=date(2025, 1, 1),
            status=self.status,
            transaction_type=self.income_type,
            category=self.expense_category,  # Категория для расходов
            subcategory=self.income_subcategory,
            amount=1000
        )
        
        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_invalid_subcategory_category_validation(self):
        """Тест валидации несоответствия подкатегории и категории"""
        transaction = Transaction(
            date=date(2025, 1, 1),
            status=self.status,
            transaction_type=self.expense_type,
            category=self.expense_category,
            subcategory=self.income_subcategory,  # Подкатегория для другой категории
            amount=1000
        )
        
        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_required_fields_validation(self):
        """Тест валидации обязательных полей"""
        transaction = Transaction(
            date=None,  # Обязательное поле
            status=self.status,
            transaction_type=self.income_type,
            category=self.income_category,
            subcategory=self.income_subcategory,
            amount=1000
        )
        
        with self.assertRaises(ValidationError):
            transaction.full_clean()