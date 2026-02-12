from django import forms
from .models import Post, Category
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):

    text = (forms.CharField(
        min_length=10,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Текст публикации'})))
        # widget = forms.Textarea(attrs={'class': 'form-textarea', 'rows': 10,  'cols': 50, 'placeholder': 'Текст публикации'})))

    categorys = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Используем чекбоксы для выбора нескольких категорий
        label='Категории',
        required=True  # Можно ли создать пост без категории? Если да, то False. Если нет, то True.
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'categorys', 'image']

        labels = {
            'title': 'Заголовок',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'article_or_news': forms.TextInput(attrs={'disabled': True})
        }

    # 'article_or_news': forms.HiddenInput()
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Название не должно быть идентично тексту статьи или новости."
            )
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы."
            )
        return cleaned_data




 # article_or_news = forms.CharField(disabled=True)


    # author = forms.ModelChoiceField(
    #     queryset=Author.objects.all(),
    #     label='Автор',
    #     empty_label='любой'
    # )