from django import forms
from transaction.models import Transaction

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ["amount"]

#     # def __init__(self, *args, **kwargs):
#     #     self.account = kwargs.get("account")
#     #     super().__init__(*args, **kwargs)
    
#     def save(self, commit=False):
#         self.instance.account = self.account
#         self.instance.balance_after_borrowed = self.account.balance
#         return super().save()


class DepositeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount"]
        
    def save(self, commit=False):
        self.instance.account = self.account
        self.instance.balance_after_borrowed = self.account.balance
        return super().save()