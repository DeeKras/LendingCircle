from django.shortcuts import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.generic import View, ListView, CreateView,  UpdateView, DeleteView, DetailView

from datetime import date, datetime, timedelta

from forms import UserProfileForm, UserForm, BorrowForm, BorrowedItemsForm, RequestReportsForm, ReturnItemForm
from models import Borrowed_Item, BorrowTransaction, UserProfile

def user_login(request):
    #login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'lendborrow/login.html', {})


def index(request):
    template_to_use = 'lendborrow/home.html'
    context = {}

    if request.method == 'POST':
        if 'New User' in request.POST['submitted']:
            registered = False
            context={'user_form': UserForm(),
                     'profile_form': UserProfileForm(),
                     'registered': registered,
                     'mode': 'new user'}
            template_to_use = 'lendborrow/register.html'

        elif 'Edit User' in request.POST['submitted']:
            context={'logged_in_as': request.user,
                     'user_form': UserForm(),
                     'profile_form': UserProfileForm(),
                     'mode': 'edit user',
                     'user':request.user}
            template_to_use = 'lendborrow/register.html'

        elif 'New Borrow' in request.POST['submitted']:
            context={'logged_in_as': request.user,
                     'borrow_form': BorrowForm(),
                     'borrowed_items_form': BorrowedItemsForm(),
                     'mode': 'new borrow'}
            template_to_use = 'forms/borrow.html'

        elif 'Edit Borrow' in request.POST['submitted'] or 'Return Item' in request.POST['submitted']:
            logged_in_as = request.user
            all_open_borroweds = Borrowed_Item.objects.filter(borrow_transaction__lender=logged_in_as)\
                                                    .filter(borrowed_status='Open')
            context={'logged_in_as': request.user,
                     'mode': request.POST['submitted'],
                     'borroweds': all_open_borroweds}
            template_to_use = 'forms/select_record.html'


        elif 'Request Report' in request.POST['submitted']:

            context = {'logged_in_as': request.user,
                       'form': RequestReportsForm}
            template_to_use = 'forms/request_report.html'

    else:
        if request.user:
            context = {'logged_in_as': request.user}
        template_to_use = 'lendborrow/home.html'

    return render(request, template_to_use, context)

def record_selected(request):  #TODO:  can this be done as a GET
    if "item to edit" in request.POST['submitted']:
        to_edit = Borrowed_Item.objects.get(id=request.POST['item_id'])
        form = BorrowedItemsForm(instance=to_edit)
        context = {'logged_in_as': request.user,
                   'form': form,
                   'borrowed': to_edit }
        template_to_use = 'forms/edit_borrowed.html'

    elif "item to return" in request.POST['submitted']:
        to_return = Borrowed_Item.objects.get(id=request.POST['item_id'])
        form = ReturnItemForm(instance=to_return)
        context = {'logged_in_as': request.user,
                   'form': form,
                   'to_return': to_return}
        template_to_use = 'forms/record_item_returned.html'

    return render(request, template_to_use, context)


def display_reports(request):
    logged_in_as = request.user
    borroweds = Borrowed_Item.objects.filter(borrow_transaction__borrower=logged_in_as)

    if request.POST['report']=='lent report':
        mode = 'lent'
        if request.POST['from_to']:
            borroweds = borroweds.filter(borrow_transaction__borrower=request.POST['from_to'])

    elif request.POST['report']=='borrowed report':
        mode = 'borrowed'
        if request.POST['from_to']:
            borroweds = borroweds.filter(borrow_transaction__lender=request.POST['from_to'])

    if request.POST['status']=='All':
        borroweds = borroweds
    else:
        borroweds = borroweds.filter(borrowed_status=request.POST['status'])

    if request.POST['start_date'] and request.POST['end_date']:
        borroweds = borroweds.filter(borrow_transaction__borrowed_date__range=(start_date, end_date))

    context={'borroweds': borroweds,
              'logged_in_as': logged_in_as,
              'mode': mode,
              }
    template_to_use = 'reports/report.html'
    return render(request, template_to_use, context)



def register(request):
    registered = False

    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.save_initials()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'lendborrow/register.html',
            {'user_form': user_form,
             'profile_form': profile_form,
             'registered': registered},
            )


def borrow(request):
    if request.method == 'POST':
        if 'new' in request.POST['mode']:
            form = BorrowForm(request.POST)
            borrowed_transaction = form.save(commit=False)
            borrowed_transaction.lender = request.user
            borrowed_transaction.save()

        form = BorrowedItemsForm(request.POST)
        if form.is_valid():
            if 'new' in request.POST['mode']:
                borrowed_item = form.save(commit=False)
                borrow_trans_id = BorrowTransaction.objects.get(id=borrowed_transaction.id)
                borrowed_item.borrow_transaction = borrow_trans_id
                borrowed_item.item_is_borrowed()
                borrowed_item.save()
                return redirect('/')
            elif 'edit' in request.POST['mode']:
                editted_item = Borrowed_Item.objects.get(id=request.POST['item_id'])
                editted_item.item_category = request.POST['item_category']
                editted_item.item_short_desc = request.POST['item_short_desc']
                editted_item.item_detail_desc = request.POST['item_detail_desc']
                editted_item.borrowed_condition = request.POST['borrowed_condition']
                editted_item.borrowed_comment = request.POST['borrowed_comment']
                editted_item.send_borrower_reminder = request.POST['send_borrower_reminder']
                editted_item.borrowed_status = request.POST['borrowed_status']
                editted_item.expected_return_date = request.POST['expected_return_date']

                editted_item.save()

                if 'Cancelled' in request.POST['borrowed_status']:
                    editted_item.borrow_is_cancelled()
                elif 'Forgiven' in request.POST['borrowed_status']:
                    editted_item.borrow_is_forgiven()

            return redirect('/')


        else:
            print 'form is not valid'

    else:
        context={'borrow_form': Borrow(),
                 'borrowed_items_form': BorrowedItemsForm(),
                 'mode': 'new borrow',
                 'lender': request.user}
        template_to_use = 'forms/borrow.html'

    return render(request, template_to_use, context)

def returned(request):
    if request.method == 'POST':
        form = ReturnItemForm(request.POST)
        if form.is_valid():
            returned_item = Borrowed_Item.objects.get(id=request.POST['item_id'])
            returned_item.returned_comment = request.POST['returned_comment']
            returned_item.returned_condition = request.POST['returned_condition']
            returned_item.save()
            returned_item.item_is_returned()

            return redirect('/')
        else:
            print 'form is not valid'
    else:
        context={'mode': 'returning',
                 'lender': request.user}
        template_to_use = 'forms/record_item_returned.html'

    return render(request, template_to_use, context)
