
from django.urls import path
from accounts.views import RegistrationView, UserLogIn, AccountUpdate, LogOut, Profile, SetImage, EditProfile, ChangePassword, ReturnBook

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", UserLogIn.as_view(), name="log_in"),
    path("update-account/", AccountUpdate.as_view(), name="update_account"),
    path('logout/', LogOut, name="log_out"),
    path("profile/", Profile, name="profile"),
    # path("profile/", BookList.as_view(), name="profile"),
    path("set-image/", SetImage, name="image"),
    path("edit-profile/", EditProfile.as_view(), name="edit_profile"),
    path("change-password/", ChangePassword, name="password"),
    path("return-book/<int:id>/", ReturnBook, name="return"),
]