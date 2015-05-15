from models import UserProfile, BorrowTransaction, Borrowed_Item
from django.contrib.auth.models import User
from django import forms



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

class BorrowedItemsForm(forms.ModelForm):
    class Meta:
        model = Borrowed_Item
        exclude = ('returned_date', 'returned_condition', 'returned_comment')
        widgets = {'borrowed_status': forms.Select(choices=Borrowed_Item.BORROWED_STATUS)}  #TODO: Can I select only some choices from this list of choices?

class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = Borrowed_Item
        fields = ('returned_condition', 'returned_comment')
        widgets = {'returned_condition': forms.Select(choices=Borrowed_Item.ITEM_CONDITIONS_CHOICES)}

class RequestReportsForm(forms.Form):
    REPORT_CHOICES = (
        ('',''),
        ('lent report', 'Who I LENT to'),
        ('borrowed report', 'Who I BORROWED from'),
    )
    report = forms.CharField(max_length=1,
                widget=forms.Select(choices=REPORT_CHOICES),
                required=True)
    from_to = forms.ModelChoiceField(User.objects.all(),
                                     label='Borrowed from OR Lent to')

        #TODO: Make this a queryset of all who this person lent/ borrowed from.
        #maybe something like this: creator_choices = [(c.id, c.username) for c in Group.objects.get(name__icontains='creator').user_set.all()]
    start_date = forms.DateField() #TODO: jquery widget datepicker
    end_date = forms.DateField() #TODO: jquery widget datepicker
    status = forms.CharField(max_length=9,
                widget=forms.Select(choices=Borrowed_Item.BORROWED_STATUS))



