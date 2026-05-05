from django import forms
from django.forms import ModelForm, TextInput, Select
from .models import Quote, Author,Tag

class QuoteForm(ModelForm):
    tags = forms.CharField(
        max_length=200,
        required=False,
        widget=TextInput(attrs={
            "class": "form-control",
            "id": "quoteTags",
            "placeholder": "Теги через кому (наприклад: life, happiness)"
        })
    )

    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        widget=Select(attrs={
            "class": "form-control",
            "id": "authorName"
        }),
        empty_label="Оберіть автора"
    )

    class Meta:
        model = Quote
        fields = ['quote', 'author']
        widgets = {
            'quote': TextInput(attrs={
                "class": "form-control",
                "id": "quoteText",
                "placeholder": "Введіть цитату"
            }),
        }

    def save(self, commit=True):
        quote = super().save(commit=commit)

        # обробка тегів вручну
        tags_str = self.cleaned_data.get("tags", "")
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                quote.tags.add(tag)

        return quote


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['author_fullname', 'born_date', 'born_location', 'description']
        widgets = {
            'author_fullname': TextInput(attrs={
                "class": "form-control",
                "id": "authorFullname",
                "placeholder": "Повне ім'я автора"
            }),
            'born_date': TextInput(attrs={
                "class": "form-control",
                "id": "bornDate",
                "placeholder": "Дата народження (наприклад: 12 June 1804)"
            }),
            'born_location': TextInput(attrs={
                "class": "form-control",
                "id": "bornLocation",
                "placeholder": "Місце народження"
            }),
            'description': TextInput(attrs={
                "class": "form-control",
                "id": "description",
                "placeholder": "Опис(Не обов'язково)"
            })
        }
