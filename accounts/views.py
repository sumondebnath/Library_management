from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from accounts.forms import ImageForm, UserRegistrationForm, UserUpdateForm
from accounts.models import UserAccount
from book.models import BorrowBooK

# import logging

# logger = logging.getLogger(__name__)


# Create your views here.

def send_transaction_mail(user, amount, subject, template):
    if not user.email:
        return

    # try:
    message = render_to_string(template, {
        "user": user,
        "amount": amount,
    })
    send_mail = EmailMultiAlternatives(subject, "", to=[user.email])
    send_mail.attach_alternative(message, "text/html")
    send_mail.send()

    # except Exception:
    #     logger.exception(
    #         "Failed to send email to %s: %s",
    #         user.email,
    #         subject,
    #     )


class RegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = UserRegistrationForm

    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_transaction_mail(self.request.user, None, "Registration", "accounts/registration_mail.html")
        return super().form_valid(form)


class UserLogIn(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        send_transaction_mail(self.request.user, None, "Log In", "accounts/login_mail.html")
        return reverse_lazy("home")


def LogOut(request):
    logout(request)
    return redirect("log_in")


@login_required
def Profile(request):
    user = request.user.account

    book = BorrowBooK.objects.filter(borrowUser=request.user)
    return render(request, "accounts/profile.html", {"usr": user, "books": book})


@login_required
def SetImage(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            account = request.user.account
            account.image = form.cleaned_data['image']
            account.save()
            return redirect("profile")
    else:
        form = ImageForm()
    return render(request, "accounts/set_image.html", {"form": form})


class EditProfile(LoginRequiredMixin, View):
    template_name = "accounts/edit_profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserUpdateForm(self.request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(request, self.template_name, {"form": form})


@login_required
def ChangePassword(request):
    if request.method == "POST":
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully.")
            return redirect("home")
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, "accounts/password.html", {"form": form})


@login_required
def ReturnBook(request, id):
    book = get_object_or_404(BorrowBooK, id=id, borrowUser=request.user)
    account = request.user.account
    account.balance += book.borrowBook.borrowed_price
    account.save()
    book.delete()
    send_transaction_mail(request.user, None, "Returned Book", "accounts/return_mail.html")
    return redirect("home")
