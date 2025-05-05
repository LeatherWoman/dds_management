from django.db import models
from django.core.exceptions import ValidationError
from typing import Optional, List, Dict, Any

class Status(models.Model):
    """Модель для статусов транзакций (Бизнес, Личное, Налог и т.д.)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название статуса")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class TransactionType(models.Model):
    """Модель для типов транзакций (Пополнение, Списание)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Тип операции")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"


class Category(models.Model):
    """Модель для категорий транзакций"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Тип операции"
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.transaction_type})"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('name', 'transaction_type')


class SubCategory(models.Model):
    """Модель для подкатегорий транзакций"""
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория"
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ('name', 'category')


class Transaction(models.Model):
    """Основная модель для учета движения денежных средств"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    date = models.DateField(verbose_name="Дата операции")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        verbose_name="Тип операции"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Сумма"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def clean(self) -> None:
        """Валидация логических зависимостей"""
        if self.category.transaction_type != self.transaction_type:
            raise ValidationError(
                "Выбранная категория не относится к выбранному типу операции"
            )
        
        if self.subcategory.category != self.category:
            raise ValidationError(
                "Выбранная подкатегория не относится к выбранной категории"
            )

    def save(self, *args, **kwargs) -> None:
        """Переопределение save с вызовом clean для валидации"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.date} - {self.transaction_type} {self.amount}р."

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-date']