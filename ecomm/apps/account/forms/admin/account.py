from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm,
)
from ecomm.apps.account.models import Account

class AccountCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('username', 'email')

class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('username', 'email')