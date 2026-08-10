from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.views import send_transaction_mail
from transaction.forms import DepositeForm
from transaction.models import Transaction

# Create your views here.

@login_required
def Deposite(request):
    if request.method == "POST":
        form = DepositeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            account = request.user.account
            account.balance += amount
            account.save()
            Transaction.objects.create(
                account=account,
                amount=amount,
                balance_after_borrowed=account.balance,
            )
            messages.success(request, "Deposited Successfully.")
            send_transaction_mail(request.user, None, "Deposite money", "transaction/deposite_mail.html")
            return redirect('home')
    else:
        form = DepositeForm()
    return render(request, "transaction/deposite.html", {"form": form})
