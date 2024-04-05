from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from Frontend.models import CustomUser,UserProfile,BookSlotDB


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    username = forms.CharField(label='Username')

    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']



class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=100)



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','phone','email','place','profile_picture']


class BookSlotForm(forms.ModelForm):
    class Meta:
        model = BookSlotDB
        fields = ['UserName','TheatreName','TheatreAddress','MovieName','SeatNum','Date','Time','TotalPrice']



class SearchForm(forms.Form):
    query = forms.CharField(label='Search')