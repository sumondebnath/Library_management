from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import UserAccount
from accounts.constants import GENDER_TYPE, USER_TYPE

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    user_type = forms.ChoiceField(choices=USER_TYPE)
    # image = forms.FileField(widget=forms.FileInput())

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "birth_date", "gender", "user_type"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            birth_date = self.cleaned_data.get("birth_date")
            gender = self.cleaned_data.get("gender")
            user_type = self.cleaned_data.get("user_type")
            # image = self.cleaned_data.get("image")

            UserAccount.objects.create(
                user = user,
                birth_date = birth_date,
                gender = gender,
                user_type=user_type,
                # image=image,
            )
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class" : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
    

class ImageForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ["image"]



class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    user_type = forms.ChoiceField(choices=USER_TYPE)
    # image = forms.FileField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class" : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

        if self.instance:
            try:
                user_account = self.instance.account
            except UserAccount.DoesNotExist:
                user_account = None
                
            if user_account:
                self.fields["birth_date"].initial = user_account.birth_date
                self.fields["gender"].initial = user_account.gender
                self.fields["user_type"].initial = user_account.user_type
                # self.fields["image"].initial = user_account.image

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserAccount.objects.get_or_create(user=user)

            user_account.birth_date = self.cleaned_data["birth_date"]
            user_account.gender = self.cleaned_data["gender"]
            user_account.user_type = self.cleaned_data["user_type"]
            # user_account.image = self.cleaned_data["image"]
            user_account.save()
        return user