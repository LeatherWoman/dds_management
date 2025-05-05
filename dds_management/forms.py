from django import forms
from typing import Dict, Any
from .models import (
    Transaction,
    Status,
    TransactionType,
    Category,
    SubCategory
)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы для всех полей
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Фильтрация подкатегорий при редактировании
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        
        if category and subcategory:
            if subcategory.category != category:
                raise forms.ValidationError("Выбранная подкатегория не принадлежит выбранной категории")
        
        return cleaned_data


class StatusForm(forms.ModelForm):
    """Форма для управления статусами"""
    class Meta:
        model = Status
        fields = ['name']


class TransactionTypeForm(forms.ModelForm):
    """Форма для управления типами транзакций"""
    class Meta:
        model = TransactionType
        fields = ['name']


class CategoryForm(forms.ModelForm):
    """Форма для управления категориями"""
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']


class SubCategoryForm(forms.ModelForm):
    """Форма для управления подкатегориями"""
    class Meta:
        model = SubCategory
        fields = ['name', 'category']