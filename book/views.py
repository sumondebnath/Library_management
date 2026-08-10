from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView

from accounts.views import send_transaction_mail
from book.forms import ReviewForm
from book.models import Book, BorrowBooK


class Detail_view(DetailView):
    model = Book
    template_name = "book/details.html"
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        post = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = post
            new_review.save()
            messages.success(request, "Thanks for your review.")
        else:
            self.review_form = review_form
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        reviews = post.reviews.all()
        review_form = getattr(self, "review_form", None) or ReviewForm()

        already_borrowed = (
            self.request.user.is_authenticated
            and BorrowBooK.objects.filter(borrowUser=self.request.user, borrowBook=post).exists()
        )

        context["reviews"] = reviews
        context["review_form"] = review_form
        context["already_borrowed"] = already_borrowed
        return context


@login_required
def BorrowBookView(request, id):
    account = request.user.account
    book = get_object_or_404(Book, id=id)

    if account.balance >= book.borrowed_price:
        if BorrowBooK.objects.filter(borrowUser=request.user, borrowBook=book).exists():
            messages.warning(request, "You already borrowed this book.")
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
