import django_filters
from django import forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Author

# Создаем свой набор фильтров для модели Product.

class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label = 'Автор',
        empty_label='любой'
    )
    # title = django_filters.CharFilter()
    # Фильтрация по диапазону дат "от"
    time_in_after = django_filters.DateFilter(
        field_name='time_in',
        lookup_expr='date__gte',  # Greater than or equal to (больше или равно)
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата поста от'
    )
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {'title'}
    # # Фильтрация по точной дате (для выбора одного конкретного дня)
    # time_in_exact = django_filters.DateFilter(
    #     field_name='time_in',
    #     lookup_expr='date',  # Важно: извлекает только дату из DateTimeField
    #     widget=forms.DateInput(attrs={'type': 'date'}),  # HTML5 виджет календаря
    #     label='Дата поста (точно)'
    # )

    # # Фильтрация по диапазону дат "до"
    # time_in_before = django_filters.DateFilter(
    #     field_name='time_in',
    #     lookup_expr='date__lte',  # Less than or equal to (меньше или равно)
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     label='Дата поста до'
    # )



