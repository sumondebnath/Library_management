from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from transaction.forms import DepositeForm
from accounts.models import UserAccount
from transaction.models import Transaction
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.views import send_transaction_mail

# Create your views here.

@login_required
def Deposite(request):
    if request.method == "POST":
        form = DepositeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get("amount")
            account = request.user.account
            # print(amount)
            account.balance += amount
            account.save()
            # form.save()
            messages.success(request, "Deposited Successfully.")
            send_transaction_mail(request.user, None, "Deposite money", "transaction/deposite_mail.html")
            return redirect('home')
    else:
        form = DepositeForm()
    return render(request, "transaction/deposite.html", {"form":form})

