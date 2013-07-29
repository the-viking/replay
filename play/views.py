from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from exchange.models import Item
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

URL = 'http://replay-project.net/'

def home(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('pwd', ''):
            errors.append('Enter a password.')
        if not request.POST.get('identity', ''):
            errors.append('Enter a username.')
        if not errors:
            username = request.POST['identity']
            password = request.POST['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    errors.append('Disabled account')
            else:
                errors.append('Wrong username or password')
    if request.user.is_authenticated():
        return render(request, 'items_allitems.html', { 'id' : request.user.id, 'items' : Item.objects.all() })
    else:
	    return render(request, 'index.html', { 'errors' : errors })

# view to access items
def item(request, num):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
    # make sure inputted id is an integer
        try:
            offset = int(num)
        except ValueError:
            raise Http404()

    # try to get this item from the database, give an error message if it doesn't exist 
        try:
            item = Item.objects.get(id=num)
            owner= User.objects.get(id=item.offered_by.id)
            yours = int(num) == owner.id
        except ObjectDoesNotExist:
            item = False
            owner = False
            yours = False
        return render(request, 'view_item.html', {'owner' : owner, 'item' : item, 'yours' : yours })

def edit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        return HttpResponseRedirect(URL)

def delete(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        return HttpResponseRedirect(URL)

def user(request, num): 
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        try:
            offset = int(num)
        except ValueError:
            raise Http404()

        try:
            user = User.objects.get(id=num)
            items = Item.objects.filter(offered_by_id=num)
            yours = user.id == int(num)
        except ObjectDoesNotExist:
            user = False
        return render(request, 'items_mypage.html', { 'user' : user, 'items' : items, 'yours' : yours })


def add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        errors = []
        id = 0
        if request.method == 'POST':
            if not request.POST.get('name', ''):
                errors.append('Enter a name.')
            if not request.POST.get('desc', ''):
                errors.append('Enter a description.')
            if not errors:
                item = Item(name=request.POST['name'], description=request.POST['desc'], offered_by = request.user, image=request.FILES['url'] )
                item.save()
                id = item.id
            form = bool(errors)
        return render(request, 'add.html', { 'id' : id, 'uid' : request.user.id, 'errors' : errors, 'form' : form})

def added(request):
    now = datetime.datetime.now()
    user = User.objects.get(id=1)
    errors = []
    if 'title' in request.POST and request.POST['title']:
        title = request.POST['title']
        if 'url' in request.POST and request.POST['url']:
            url = request.POST['title']
            if 'usn' in request.POST and request.POST['usn']:
                usn = request.POST['usn']
                if 'descr' in request.POST and request.POST['descr']:
                    desc = request.POST['descr']
                    new_item = Item(name = title, offered_date = now, description = desc, image = url, offered_by = user)
                    new_item.save()
                    link = "../item/" + str(new_item.id)
                    return render(request, 'added.html', {'id_link' : link, 'title' : title})
                else:
                    errors.append("Please enter a description.")
            else:
                errors.append("Please enter a username.")
        else:
            errors.append("Please enter a URL.")
    else:
        errors.append("Please enter a title")

    return render(request, 'added.html', {'errors' : errors})

def all_items(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        list_items = Item.objects.all()
        return render(request, 'all.html', {'items' : list_items})
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(URL) 

def account(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        return HttpResponseRedirect(URL) 

def community(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        users = User.objects.all()
        return render(request, 'community_friends.html', {'users' : users })

def my_page(request):
    return HttpResponseRedirect(URL)
