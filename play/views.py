from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from exchange.models import Item, Notification
from stickies.models import Sticky
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import settings
from django.utils.html import strip_tags

# dajax things
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

# site url, used for redirecting to homepage
URL = 'http://replay-project.net/'

def home(request):
    """ 
    loads the home page - a login screen
    if the user isn't logged in, or a page
    displaying all the items if they are 
    """
    errors = []
    # handle log-in form
    if request.method == 'POST':
        if not request.POST.get('pwd', ''):
            errors.append('Enter a password.')
        if not request.POST.get('identity', ''):
            errors.append('Enter a username.')
        # if no errors found, authenticate and log in user
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
        notes = Notification.objects.filter(sent_to=request.user)
        noted_items = [n.item for n in notes]
        page_title = 'All Items'
        return render(request, 'all.html', { 'id' : request.user.id, 'items' : Item.objects.all(), 'noted_items': noted_items })
    else:
	    return render(request, 'index.html', { 'errors' : errors })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_item(num):
    """ 
    helper function to attempt to retrieve 
    an item of a given id string, 
    returning false if item's not found, 
    or returning the item if it is found 
    """
    try:
        id = int(num)
    except ValueError:
        raise Http404()
    try:
        item = Item.objects.get(id=id)
    except ObjectDoesNotExist:
        item = False
    return item

def item(request, num):
    """ 
    displays an item if it can be found, 
    checking whether the user currently
    owns the item or not
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
    # make sure inputted id is an integer
        item = get_item(num)
        sent = False
        note = False
        if item:
            user = User.objects.get(id=item.offered_by.id)
            yours = request.user == user
            if yours:
                notes = Notification.objects.filter(sent_to=request.user)
                noted_items = [n.item for n in notes]
                if item in noted_items:
                    note = notes.get(item=item)
        else:
            user = False
            yours = False
        return render(request, 'view_item.html', {'user' : user, 'item' : item, 'yours' : yours, 'sent' : sent, 'note': note })

def edit(request, id):
    """
    handles a form to edit the fields of
    an item, after ensuring the user 
    is the owner of the item
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        item = get_item(id)
        errors = []
        edited = False
        edit = True
        if item:
            owner= User.objects.get(id=item.offered_by.id)
            yours = request.user == owner
            if request.method == 'POST':
                if len(request.POST['name']) > 40:
                    errors.append("Please enter a shorter name")
                else:
                    item.name = strip_tags(request.POST['name'])
                if len(request.POST['desc']) > 500:
                    errors.append("Please enter a shorter description")
                else:
                    item.description = strip_tags(request.POST['desc'])
                if 'image' in request.FILES:
                    file = request.FILES['image']
                    errors = errors + invalid(file)
                    if not errors:
                        item.image = file
                if not errors:
                    item.save()
                edited = not bool(errors)
                edit = bool(errors)
        else:
            owner = False
            yours = False

        return render(request, 'view_item.html', { 'edit' : edit, 'owner' : owner, 'item' : item, 'yours' : yours, 'errors' : errors, 'edited' : edited })

def notify(request, id):
    """
    creates a Notification object
    indicating interest in the 
    given object
    """
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
    """ 
    if the user owns the item,
    deletes it from the database
    and the image from the filesystem
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        msg = ''
        item = get_item(id)
        if(item):
            if request.user == item.offered_by:
                Item.delete(item)
                msg = item.name + " deleted succesfully!"
    return render(request, 'items_mypage.html', { 'msg' : msg, 'deleted' : True })

def user(request, num): 
    """
    displays the items of a requested user,
    showing a slightly different page
    if that user is you
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        try:
            id = int(num)
        except ValueError:
            raise Http404()
        try:
            user = User.objects.get(id=id)
            items = Item.objects.filter(offered_by_id=num)
            yours = request.user.id == user.id
        except ObjectDoesNotExist:
            user = False
            items = False
            yours = False
        if not yours:
            return render(request, 'community_friends_2.html', { 'user' : user, 'id': user.id, 'items' : items })
        else: 
            notes = Notification.objects.filter(sent_to=request.user)
            noted_items = [n.item for n in notes]
            return render(request, 'items_mypage.html', { 'user' : user, 'items' : items, 'id': user.id, 'noted_items' : noted_items })


def invalid(file):
    """
    helper function for image handling views 
    to check file type (image) and size (<4.5mb)
    """
    errors = []
    file_type = file.content_type.split('/')[0]
    # check file type and size against parameters in settings file
    if file_type not in settings.TASK_UPLOAD_FILE_TYPES:
        errors.append('File type is not supported.')
    if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
        errors.append('Your image is too big.')
    return errors

def add(request):
    """
    handles a form to add an item to the
    database, ensuring all fields have
    been filled out and the image is valid
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        errors = []
        item = False
        form = True
        msg = ''
        desc = False
        name = False
        file = False
        if request.method == 'POST':
            if not request.POST.get('name', ''):
                errors.append('Enter a name.')
            else:
                name = strip_tags(request.POST['name'])
                if len(name) > 40:
                    errors.append('Enter a shorter name')
            if not request.POST.get('desc', ''):
                errors.append('Enter a description.')
            else:
                desc = strip_tags(request.POST['desc'])
                if len(desc) > 500:
                    errors.append('Enter a shorter description')
            if 'image' not in request.FILES:
                errors.append('Please submit an image')
            else:
                file = request.FILES['image']
                errors = errors + invalid(file)
            if not errors:
                item = Item(name=name, description=desc, offered_by = request.user, image=file )
                item.save()
            form = bool(errors)
        return render(request, 'add.html', { 'item' : item, 'id' : request.user.id, 'errors' : errors, 'form' : form, 'msg' : msg, 'desc':desc, 'name':name})


def logout_user(request):
    """
    calls the built-in logout
    function to log out a user
    """
    logout(request)
    return HttpResponseRedirect(URL) 

def account(request):
    """
    displays the account settings form,
    filling out every field with information
    already associated with the account.
    Upon submission, user and profile
    models are updated appropriately
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        user = request.user
        errors = []
        changed = False
        # handle form submission
        if request.method == 'POST':
            profile = user.profile
            # validate image
            if 'image' in request.FILES:
                image = request.FILES['image']
                errors = errors + invalid(image)
                if not errors: 
                    profile.picture = image
            # check which fields have been filled out,
            # set model field to their values
            if request.POST.get('name', ''):
                user.username = request.POST['name']
            if request.POST.get('phone', ''):
                profile.telephone = request.POST['phone']
            if request.POST.get('email', ''):
                user.email = request.POST['email']
            if request.POST.get('firstname', ''):
                user.first_name = request.POST['firstname']
            if request.POST.get('lastname', ''):
                user.last_name = request.POST['lastname']
            if request.POST.get('address', ''):
                profile.address = request.POST['address']
            # change password if confirmation field is correct
            if request.POST.get('pwd', ''):
                pwd = request.POST['pwd']
                if request.POST.get('pwd_conf', ''):
                    if pwd == request.POST['pwd_conf']:
                        user.password = pwd
                    else:
                        errors.append('Enter your new password again in confirmation password')
            # save the User and Profile models if no errors have been found
            if not errors:
                user.save()
                profile.save()
                changed = True
        return render(request, 'accounts.html', {'user' : user, 'errors' : errors, 'changed' : changed} )

def community(request):
    """displays all users
    on the site, linking to 
    their user pages
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        return render(request, 'community.html', {'users' : User.objects.all() })

def ask(request):
    """
    Displays all stickies,
    allows users to edit
    and add new ones
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect(URL)
    else:
        errors = []
        text = False
        if request.method == 'POST':
            if not request.POST.get('sticktext', ''):
                errors.append('Enter some text for your sticky.')
            else:
                text = request.POST['sticktext']
                if len(text) > 70:
                    errors.append('Your text is too long')
            if not errors:
               sticky = Sticky(writer = request.user, message = text) 
               sticky.save()
        return render(request, 'ask.html', {'stickies' : Sticky.objects.all(), 'errors' : errors })
