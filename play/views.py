from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from exchange.models import Item, Notification
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import settings
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

def get_item(num):
    try:
        offset = int(num)
    except ValueError:
        raise Http404()
    try:
        item = Item.objects.get(id=num)
    except ObjectDoesNotExist:
        item = False
    return item

# view to access items
def item(request, num):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
    # make sure inputted id is an integer
        item = get_item(num)
        sent = False
        if item:
            owner= User.objects.get(id=item.offered_by.id)
            yours = request.user == owner
        else:
            owner = False
            yours = False
        return render(request, 'view_item.html', {'owner' : owner, 'item' : item, 'yours' : yours, 'sent' : sent })

def edit(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        item = get_item(id)
        if item:
            owner= User.objects.get(id=item.offered_by.id)
            yours = request.user == owner
        else:
            owner = False
            yours = False
        return render(request, 'view_item.html', { 'edit' : True, 'owner' : owner, 'item' : item, 'yours' : yours })

def notify(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        item = get_item(id)
        if item:
            owner= User.objects.get(id=item.offered_by.id)
            yours = request.user == owner
            note = Notification(sent_to = owner, sent_from = request.user, item = item, visible = True)
            note.save()
            sent = True
        else:
            owner = False
            yours = False
            sent = False
        return render(request, 'view_item.html', {'owner' : owner, 'item' : item, 'yours' : yours, 'sent' : sent })

def delete(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        msg = ''
        item = get_item(id)
        if(item):
            if request.user == item.offered_by:
                Item.delete(item)
                msg = item.name + " deleted succesfully!"
    return render(request, 'items_mypage.html', { 'msg' : msg })

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
            yours = request.user.id == user.id
        except ObjectDoesNotExist:
            user = False
            items = False
            yours = False
        if not yours:
            return render(request, 'community_friends_2.html', { 'user' : user, 'items' : items })
        else: 
            return render(request, 'items_mypage.html', { 'user' : user, 'items' : items })


def add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        errors = []
        item = False
        form = True
        msg = ''
        desc = False
        name = False
        if request.method == 'POST':
            if not request.POST.get('name', ''):
                errors.append('Enter a name.')
            else:
                name = request.POST['name']
            if not request.POST.get('desc', ''):
                errors.append('Enter a description.')
            else:
                desc = request.POST['desc']
            if 'image' not in request.FILES:
                errors.append('Please submit an image')
            else:
                file = request.FILES['image']
                errors = errors + invalid(file)  
            if not errors:
                item = Item(name=name, description=desc, offered_by = request.user, image=file )
                item.save()
                id = item.id
            form = bool(errors)
        return render(request, 'add.html', { 'item' : item, 'uid' : request.user.id, 'errors' : errors, 'form' : form, 'msg' : msg, 'desc':desc, 'name':name})

# helper function for image handling views to check file type and size
def invalid(file):
    errors = []
    file_type = file.content_type.split('/')[0]
    if file_type not in settings.TASK_UPLOAD_FILE_TYPES:
        errors.append('File type is not supported.')
    if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
        errors.append('Your image is too big.')
    return errors

def all_items(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        return render(request, 'all.html', {'items' : Item.objects.all()})
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(URL) 

def account(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        user = request.user
        if request.method == 'POST':
            profile = user.profile
            if 'image' in reqest.FILES:
                image = request.FILES['image']
                errors = invalid(image)
                if not errors: 
                    profile.picture = image
            user.save()
            profile.save()
        return render(request, 'accounts.html', {'user' : user} )

def community(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        return render(request, 'community_friends.html', {'users' : User.objects.all() })
