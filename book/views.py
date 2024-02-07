from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from book.models import Book, BorrowBooK
from book.forms import ReviewForm
from accounts.models import UserAccount
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.views import send_transaction_mail


class Detail_view(DetailView):
    model= Book
    template_name = "book/details.html"
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        post = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = post
            new_review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        reviews = post.reviews.all()
        review_form = ReviewForm()

        context["reviews"] = reviews
        context["review_form"] = review_form
        return context


@login_required
def BorrowBookView(request, id):
    account = request.user.account
    # balance = account.balance
    book = Book.objects.get(id = id)

    if book.borrowed_price < account.balance:
        if BorrowBooK.objects.filter(borrowUser=request.user, borrowBook=book).exists():
           messages.warning(request, "You already borrowed this book.")
        # except BorrowBooK.objects.get(id=id).DoesNotExist:
        else:
            BorrowBooK.objects.create(borrowUser=request.user, borrowBook=book)
            account.balance -= book.borrowed_price
            account.save()
            messages.success(request, "You Borrow The Book.")
            send_transaction_mail(request.user, None, "Borrow Book", "book/borrow_mail.html")
            return HttpResponseRedirect(reverse_lazy("home"))
    else:
        messages.error(request, "Your Balance is Lower than Book Price.")
    return HttpResponseRedirect(reverse_lazy("home"))