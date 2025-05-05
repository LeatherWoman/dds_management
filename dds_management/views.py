from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.exceptions import ValidationError
from django.db.models import Q
from typing import Optional, Dict, Any
from datetime import date
from .models import (
    Transaction,
    Status,
    TransactionType,
    Category,
    SubCategory
)
from .forms import (
    TransactionForm,
    StatusForm,
    TransactionTypeForm,
    CategoryForm,
    SubCategoryForm
)

class TransactionListView(ListView):
    model = Transaction
    template_name = 'dds_management/index.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.GET

        # Фильтрация по дате
        if params.get('date_from'):
            queryset = queryset.filter(date__gte=params['date_from'])
        if params.get('date_to'):
            queryset = queryset.filter(date__lte=params['date_to'])

        # Фильтрация по статусу
        if params.get('status'):
            queryset = queryset.filter(status_id=params['status'])

        # Фильтрация по типу операции
        if params.get('transaction_type'):
            queryset = queryset.filter(transaction_type_id=params['transaction_type'])

        # Фильтрация по категории
        if params.get('category'):
            queryset = queryset.filter(category_id=params['category'])

        # Фильтрация по подкатегории
        if params.get('subcategory'):
            queryset = queryset.filter(subcategory_id=params['subcategory'])

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'statuses': Status.objects.all(),
            'transaction_types': TransactionType.objects.all(),
            'categories': Category.objects.all(),
            'subcategories': SubCategory.objects.filter(
                category_id=self.request.GET.get('category')
            ) if self.request.GET.get('category') else SubCategory.objects.none()
        })
        return context


class TransactionCreateUpdateView(View):
    """Представление для создания и обновления транзакций с полной обработкой ошибок"""
    template_name = 'dds_management/transaction_form.html'
    success_url = 'dds_management:transaction_list'
    
    def get(self, request, pk: Optional[int] = None):
        """Обработка GET-запроса (отображение формы)"""
        try:
            if pk:
                transaction = get_object_or_404(Transaction, pk=pk)
                form = TransactionForm(instance=transaction)
            else:
                form = TransactionForm(initial={'date': date.today()})
            
            return render(request, self.template_name, {
                'form': form,
                'is_edit': pk is not None
            })
            
        except Exception as e:
            # Логирование ошибки (можно добавить logger.error здесь)
            form = TransactionForm()
            return render(request, self.template_name, {
                'form': form,
                'error_message': f'Ошибка при загрузке формы: {str(e)}'
            })

    def post(self, request, pk: Optional[int] = None):
        """Обработка POST-запроса (сохранение данных)"""
        try:
            if pk:
                transaction = get_object_or_404(Transaction, pk=pk)
                form = TransactionForm(request.POST, instance=transaction)
            else:
                form = TransactionForm(request.POST)
            
            if form.is_valid():
                try:
                    transaction = form.save()
                    return redirect(self.success_url)
                except ValidationError as e:
                    # Добавляем ошибки валидации в форму
                    for field, errors in e.error_dict.items():
                        for error in errors:
                            form.add_error(field, error)
                except Exception as e:
                    # Обработка других ошибок при сохранении
                    form.add_error(None, f'Ошибка при сохранении: {str(e)}')
            
            # Если форма не валидна или возникла ошибка
            return render(request, self.template_name, {
                'form': form,
                'is_edit': pk is not None,
                'error_message': 'Пожалуйста, исправьте ошибки в форме'
            })
            
        except Exception as e:
            # Обработка непредвиденных ошибок
            form = TransactionForm(request.POST)
            return render(request, self.template_name, {
                'form': form,
                'is_edit': pk is not None,
                'error_message': f'Произошла ошибка: {str(e)}'
            })


class TransactionDeleteView(View):
    """Представление для удаления транзакций"""
    def post(self, request, pk: int):
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.delete()
        return redirect('dds_management:transaction_list')


class ReferenceManagementView(View):
    """Представление для управления справочниками"""
    template_name = 'dds_management/reference_management.html'
    
    def get(self, request):
        context = {
            'status_form': StatusForm(),
            'transaction_type_form': TransactionTypeForm(),
            'category_form': CategoryForm(),
            'subcategory_form': SubCategoryForm(),
            'statuses': Status.objects.all(),
            'transaction_types': TransactionType.objects.all(),
            'categories': Category.objects.all(),
            'subcategories': SubCategory.objects.all(),
        }
        return render(request, self.template_name, context)


class ReferenceCreateView(View):
    """Представление для создания записей в справочниках"""
    def post(self, request, model_name: str):
        forms_map = {
            'status': StatusForm,
            'transaction_type': TransactionTypeForm,
            'category': CategoryForm,
            'subcategory': SubCategoryForm,
        }
        
        form_class = forms_map.get(model_name)
        if not form_class:
            return redirect('dds_management:reference_management')
        
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
        
        return redirect('dds_management:reference_management')


class ReferenceDeleteView(View):
    """Представление для удаления записей из справочников"""
    def post(self, request, model_name: str, pk: int):
        models_map = {
            'status': Status,
            'transaction_type': TransactionType,
            'category': Category,
            'subcategory': SubCategory,
        }
        
        model_class = models_map.get(model_name)
        if not model_class:
            return redirect('dds_management:reference_management')
        
        item = get_object_or_404(model_class, pk=pk)
        item.delete()
        
        return redirect('dds_management:reference_management')
    

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)