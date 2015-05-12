from models import UserProfile, BorrowTransaction, Borrowed_Item
from django.contrib.auth.models import User
from django import forms
from django.forms.models import modelformset_factory

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('cell_phone', 'location')

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowTransaction
        fields = ('borrower',)

BorrowFormSet = modelformset_factory(Borrowed_Item,
                                     exclude=('borrowed_status', 'returned_date', 'returned_condition', 'returned_comment'),
                                     extra=1,
                                     )

class BorrowedItems(forms.ModelForm):
    class Meta:
        model = Borrowed_Item
        exclude = ('borrowed_status', 'returned_date', 'returned_condition', 'returned_comment')

