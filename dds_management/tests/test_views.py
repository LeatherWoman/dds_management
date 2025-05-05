from django.test import TestCase, RequestFactory
from django.urls import reverse
from datetime import date
from dds_management.models import (
    Status,
    TransactionType,
    Category,
    SubCategory,
    Transaction
)
from dds_management.views import TransactionListView

class TransactionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.status = Status.objects.create(name="Бизнес")
        cls.income_type = TransactionType.objects.create(name="Пополнение")
        cls.category = Category.objects.create(
            name="Продажи",
            transaction_type=cls.income_type
        )
        cls.subcategory = SubCategory.objects.create(
            name="Онлайн",
            category=cls.category
        )
        
        # Создаем тестовые транзакции
        Transaction.objects.create(
            date=date(2025, 1, 1),
            status=cls.status,
            transaction_type=cls.income_type,
            category=cls.category,
            subcategory=cls.subcategory,
            amount=1000
        )
        Transaction.objects.create(
            date=date(2025, 1, 2),
            status=cls.status,
            transaction_type=cls.income_type,
            category=cls.category,
            subcategory=cls.subcategory,
            amount=2000
        )

    def setUp(self):
        self.factory = RequestFactory()

    def test_view_url_exists(self):
        """Тест доступности URL"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Тест использования правильного шаблона"""
        response = self.client.get(reverse('dds_management:transaction_list'))
        self.assertTemplateUsed(response, 'dds_management/index.html')

    def test_filtering_by_date(self):
        """Тест фильтрации по дате"""
        request = self.factory.get('/', {
            'date_from': '2025-01-02',
            'date_to': '2025-01-02'
        })
        response = TransactionListView.as_view()(request)
        self.assertEqual(len(response.context_data['transactions']), 1)
        self.assertEqual(response.context_data['transactions'][0].date, date(2025, 1, 2))

    def test_filtering_by_status(self):
        """Тест фильтрации по статусу"""
        request = self.factory.get('/', {'status': self.status.id})
        response = TransactionListView.as_view()(request)
        self.assertEqual(len(response.context_data['transactions']), 2)

    def test_filtering_by_category(self):
        """Тест фильтрации по категории"""
        request = self.factory.get('/', {'category': self.category.id})
        response = TransactionListView.as_view()(request)
        self.assertEqual(len(response.context_data['transactions']), 2)