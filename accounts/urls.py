
from django.urls import path
from accounts.views import RegistrationView, UserLogIn, LogOut, Profile, SetImage, EditProfile, ChangePassword, ReturnBook

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", UserLogIn.as_view(), name="log_in"),
    path('logout/', LogOut, name="log_out"),
    path("profile/", Profile, name="profile"),
    path("set-image/", SetImage, name="image"),
    path("edit-profile/", EditProfile.as_view(), name="edit_profile"),
    path("change-password/", ChangePassword, name="password"),
    path("return-book/<int:id>/", ReturnBook, name="return"),
]