from django.shortcuts import *
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.views.generic import View, ListView, CreateView,  UpdateView, DeleteView, DetailView

from forms import UserProfileForm, UserForm, BorrowForm, BorrowFormSet, BorrowedItems
from models import Borrowed_Item, BorrowTransaction

def user_login(request):

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
                     'borrowed_items_form': BorrowedItems(),
                     'mode': 'new borrow'}
            template_to_use = 'lendborrow/borrow.html'

    else:
        if request.user:
            context = {'logged_in_as': request.user}
        template_to_use = 'lendborrow/home.html'

        # elif 'lent' in request.POST:
        #     lender = Person.objects.get(id=request.session['user_id'])
        #     borroweds = Borrowed.objects.filter(lender__name=lender)
        #     context = {'borroweds': borroweds,
        #                'lender': lender}
        #     template_to_use = 'borrowstuff/rpt_lent.html'
        #
        # elif 'borrowed' in request.POST:
        #     print "request.session['user_id'] {}".format(request.session['user_id'])
        #     borrower = Person.objects.get(id=request.session['user_id'])
        #     borroweds = Borrowed.objects.filter(borrower__name=borrower)
        #     context = {'borroweds': borroweds,
        #                'borrower': borrower}
        #     template_to_use = 'borrowstuff/rpt_borrowed.html'

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
        form = BorrowForm(request.POST)
        borrowed_transaction = form.save(commit=False)
        borrowed_transaction.lender = request.user
        borrowed_transaction.save()

        form = BorrowedItems(request.POST)
        if form.is_valid():
            borrowed_item = form.save(commit=False)
            borrow_trans_id = BorrowTransaction.objects.get(id=borrowed_transaction.id)
            borrowed_item.borrow_transaction = borrow_trans_id
            borrowed_item.item_is_borrowed()
            borrowed_item.save()
            return redirect('/')
        else:
            print 'form is not valid'

    else:
        context={'borrow_form': Borrow(),
                 'borrowed_items_form': BorrowedItems(),
                 'mode': 'new borrow',
                 'lender':request.user}
        template_to_use = 'lendborrow/borrow.html'

    return render(request, template_to_use, context)


#
