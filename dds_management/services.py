from typing import List, Dict, Any, Optional
from django.db.models import QuerySet
from .models import (
    Transaction,
    Status,
    TransactionType,
    Category,
    SubCategory
)

class TransactionService:
    """Сервис для работы с транзакциями"""
    @staticmethod
    def get_filtered_transactions(
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        status_id: Optional[int] = None,
        transaction_type_id: Optional[int] = None,
        category_id: Optional[int] = None,
        subcategory_id: Optional[int] = None
    ) -> QuerySet[Transaction]:
        """Получение отфильтрованного списка транзакций"""
        queryset = Transaction.objects.all()
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if transaction_type_id:
            queryset = queryset.filter(transaction_type_id=transaction_type_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)
        
        return queryset.order_by('-date')

    @staticmethod
    def create_transaction(transaction_data: Dict[str, Any]) -> Transaction:
        """Создание новой транзакции"""
        transaction = Transaction(**transaction_data)
        transaction.full_clean()
        transaction.save()
        return transaction

    @staticmethod
    def update_transaction(pk: int, transaction_data: Dict[str, Any]) -> Transaction:
        """Обновление существующей транзакции"""
        transaction = Transaction.objects.get(pk=pk)
        for field, value in transaction_data.items():
            setattr(transaction, field, value)
        transaction.full_clean()
        transaction.save()
        return transaction


class ReferenceService:
    """Сервис для работы со справочниками"""
    @staticmethod
    def get_all_references() -> Dict[str, QuerySet]:
        """Получение всех справочников"""
        return {
            'statuses': Status.objects.all(),
            'transaction_types': TransactionType.objects.all(),
            'categories': Category.objects.all(),
            'subcategories': SubCategory.objects.all(),
        }

    @staticmethod
    def create_reference_item(model_name: str, data: Dict[str, Any]) -> Any:
        """Создание записи в справочнике"""
        models_map = {
            'status': Status,
            'transaction_type': TransactionType,
            'category': Category,
            'subcategory': SubCategory,
        }
        
        model_class = models_map.get(model_name)
        if not model_class:
            raise ValueError(f"Unknown model: {model_name}")
        
        item = model_class(**data)
        item.full_clean()
        item.save()
        return item