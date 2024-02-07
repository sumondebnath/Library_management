from django import forms
from book.models import BookReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ["name", "review"]