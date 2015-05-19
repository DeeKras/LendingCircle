from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime

class UserProfile(models.Model):
    #extend the auth.User
    user = models.OneToOneField(User)
    initials = models.CharField(max_length=2, blank=True)
    cell_phone = models.CharField(max_length=25)
    location = models.CharField(max_length=50)

    borrower_score = models.IntegerField(default=50)
    lender_score = models.IntegerField(default=50)
    items_lent = models.IntegerField(default=0)
    items_lent_forgiven = models.IntegerField(default=0)
    items_lent_returned = models.IntegerField(default=0)

    items_borrowed = models.IntegerField(default=0)
    items_borrowed_forgiven = models.IntegerField(default=0)
    items_returned = models.IntegerField(default=0)

    def __unicode__(self):
        return '{} {} ({})'.format(self.user.first_name, self.user.last_name, self.location)

    def save_initials(self):
        self.initials = '{}{}'.format(self.user.first_name[0], self.user.last_name[0])
        self.save()

class BorrowTransaction(models.Model):
    #one borrowing transaction can have several items lent to the same person
    borrowed_date = models.DateTimeField(default=timezone.now())
    lender = models.ForeignKey('auth.User', related_name='lender')
    borrower = models.ForeignKey('auth.User', related_name='borrower',
                                 error_messages={'required': 'please choose a borrower', 'null': 'NULL11!'})

    def new_borrow_transaction(self):
        Borrowed_Item.objects.create(borrow_transaction=self)

    def __unicode__(self):
        return '{0} lent to {1}: {2:%Y}_{2:%m}_{2:%d}'.format(self.lender, self.borrower, self.borrowed_date)

class Borrowed_Item(models.Model):
    # a borrow transaction can have several items lent (each as a separate line item)
    ITEM_CATEGORIES = (
        ('AP', 'Apparel - clothing, shoes, accessories'),
        ('JW', 'Jewelry'),
        ('BK', 'Book'),
        ('EL', 'Electronics'),
        ('CD', 'CDs, DVDs'),
        ('PG', 'Party Goods'),
        ('TL', 'Tools'),
        ('OT', 'other')
    )

    ITEM_CONDITIONS_CHOICES = (
        ('NW', 'New'),
        ('LN', 'Used, Like New'),
        ('VG', 'Used, Very Good'),
        ('GD', 'Used, Good'),
        ('FR', 'Used, Fair'),
        ('PR', 'Used, Poor'),
    )  #TODO is there a way to give each choice a weight or rating number / add another field?
    #  to be used for comparing borrowed condition with returned condition.

    SEND_REMINDERS_TO = (
        ('Email', 'Email'),
        ('Text', 'Text'),
        ('None', 'None'),
        ('Both', 'Both')
    )

    BORROWED_STATUS = (
        ('All', 'All Status'),
        ('Open', 'Open: Still Borrowed'),
        ('Returned', 'Returned'),
        ('Forgiven', "Forgiven: Don't expect to receive it back"),
        ('Cancelled', 'Cancelled: Was never really lent after all')
    )

    borrow_transaction = models.ForeignKey(BorrowTransaction, null=True, blank=True)
    item_category = models.CharField(max_length=2,
                                choices=ITEM_CATEGORIES)
    item_short_desc = models.CharField(max_length=255,)
    item_detail_desc = models.TextField(blank=True,)
    expected_return_date = models.DateField(null=True, blank=True)
    borrowed_condition = models.CharField(max_length=2,
                                          choices=ITEM_CONDITIONS_CHOICES)
    borrowed_comment = models.TextField(blank=True,)
    send_borrower_reminder = models.CharField(max_length=5,
                                          choices=SEND_REMINDERS_TO)
    borrowed_status = models.CharField(max_length=9,
                                       blank=True, null=True,
                                       default='Open')

    returned_date = models.DateField(blank=True, null=True)
    returned_condition = models.CharField(max_length=2,
                                          choices=ITEM_CONDITIONS_CHOICES,
                                          blank=True, null=True)
    returned_comment = models.TextField(blank=True)

    def __unicode__(self):
        return '{}'.format(self.item_short_desc)

    def item_is_borrowed(self):
        #for each item borrowed, these methods happen
        self.borrowed_status = 'Open'

        lender_profile = UserProfile.objects.get(user=self.borrow_transaction.lender)
        lender_profile.items_lent +=1
        lender_profile.save()

        borrower_profile = UserProfile.objects.get(user=self.borrow_transaction.borrower)
        borrower_profile.items_borrowed +=1
        borrower_profile.save()

    def borrow_is_cancelled(self):
        borrower_profile = UserProfile.objects.get(user=self.borrow_transaction.borrower)
        borrower_profile.items_borrowed -=1
        borrower_profile.save()

        lender_profile = UserProfile.objects.get(user=self.borrow_transaction.lender)
        lender_profile.items_lent -=1
        lender_profile.save()


    def borrow_is_forgiven(self):
        borrower_profile = UserProfile.objects.get(user=self.borrow_transaction.borrower)
        borrower_profile.items_borrowed_forgiven +=1
        borrower_profile.save()

        lender_profile = UserProfile.objects.get(user=self.borrow_transaction.lender)
        lender_profile.items_lent_forgiven +=1
        lender_profile.save()


    def item_is_returned(self):
        #after item is returned,
        self.borrowed_status = 'Returned'
        self.returned_date = timezone.now()
        self.save()

        borrower_profile = UserProfile.objects.get(user=self.borrow_transaction.borrower)
        borrower_profile.items_returned +=1
        borrower_profile.save()

        lender_profile = UserProfile.objects.get(user=self.borrow_transaction.lender)
        lender_profile.items_lent_returned +=1
        lender_profile.save()

        date_diff = ((self.returned_date.date() - self.expected_return_date).days)
        if date_diff < 0:
            print 'returned {} days EARLY. thank you!'.format(abs(date_diff))
        elif date_diff == 0:
            print 'returned on time. thank you!'
        elif date_diff >0:
            print 'returned {} days LATE. please be on time next time!'.format(abs(date_diff))



        #3. compare 'borrowed_condition' and 'returned_condition'
        #     if ==, borrower_score +=3
        #     if <, borrower_score -= (3* levels less than borrowed_condition)



