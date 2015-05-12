from django.contrib import admin
from models import UserProfile, BorrowTransaction, Borrowed_Item

admin.site.register(UserProfile)
admin.site.register(BorrowTransaction)
admin.site.register(Borrowed_Item)