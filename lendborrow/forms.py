
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from models import UserProfile, BorrowTransaction, Borrowed_Item


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
        error_messages={
            'borrower':{
                'required': 'Please choose a borrower'},
        }

        def confirm_borrower(self):
            borrower = self.cleaned_data.get('borrower')
            if not borrower:
                raise forms.ValidationError("Please choose a borrower")



class BorrowedItemsForm(forms.ModelForm):
    class Meta:
        relevant_borrowed_statuses =  [(k,v) for k,v in Borrowed_Item.BORROWED_STATUS if k in ['Open', 'Forgiven', 'Cancelled']]
        model = Borrowed_Item
        fields = ('item_category','item_short_desc', 'item_detail_desc', 'borrowed_comment', 'borrowed_status',
                    'borrowed_condition', 'expected_return_date','send_borrower_reminder')
        widgets = {'borrowed_status': forms.Select(choices=relevant_borrowed_statuses),}

class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = Borrowed_Item
        fields = ('returned_condition', 'returned_comment')
        widgets = {'returned_condition': forms.Select(choices=Borrowed_Item.ITEM_CONDITIONS_CHOICES)}

class RequestReportsForm(forms.Form):

#this code would get me only the people who borrowed from or lent to the user. BUT how do I bring the request.user into the Form
    # all_borrowers = BorrowTransaction.objects.filter(Q(lender=request.user)).values_list('borrower__username', flat=True).distinct()
    # all_lenders = BorrowTransaction.objects.filter(Q(borrower=request.user)).values_list('borrower__username', flat=True).distinct()
    # all_borrowers_lenders = all_borrowers | all_lenders

    REPORT_CHOICES = (
        ('','----'),
        ('lent report', 'What I LENT'),
        ('borrowed report', 'What I BORROWED'),
    )
    report = forms.CharField(max_length=15,
                widget=forms.Select(choices=REPORT_CHOICES),
                required=True,
                error_messages={'required': 'Please choose a report'})
    from_to = forms.ModelChoiceField(User.objects.all(),
                required=False,
                label='Borrowed from OR Lent to')

    start_date = forms.DateField(required=False) #TODO: jquery widget datepicker
    end_date = forms.DateField(required=False) #TODO: jquery widget datepicker
    status = forms.CharField(max_length=9,
                required=False,
                widget=forms.Select(choices=Borrowed_Item.BORROWED_STATUS))



