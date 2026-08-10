from django import forms
from book.models import BookReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ["name", "review"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "field-input"}),
            "review": forms.Textarea(attrs={"class": "field-input", "rows": 3}),
        }