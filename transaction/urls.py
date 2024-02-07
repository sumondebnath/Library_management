from django.urls import path
from transaction.views import Deposite


urlpatterns = [
    path("deposite/", Deposite, name="deposite"),
]