from django import forms
from transaction.models import Transaction


class DepositeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "field-input", "placeholder": "e.g. 500", "min": "0", "step": "0.01"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Enter an amount greater than zero.")
        return amount
