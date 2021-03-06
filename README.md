replay
======
A technology probe built and designed by Maria Håkansson, Erik Bonadonna and Jung-Hu Sohn, 
out of the Information Science department at Cornell University in summer of 2013.
Replay gives a community of users a space to give away things they don't need or want anymore
in a simple, informal way.


Replay is meant to explore notions of necessity and people' feelings about what things
they really need and make them happy.

![logo of sorts](https://github.com/the-viking/replay/blob/master/static/images/snakeitem.gif?raw=true)

Implementation
--------------

Replay is implemented as a Django project, with the models defined
in several custom apps (exchange, stickies, admin_extension), 
project settings in play/settings.py, url patterns in play/urls.py
view controller functions in play/views.py, and html templates in
the templates directory.

### Models ###
Models are stored in a MySQL database, accessed through Django's built in
database interface.

###### Defined in *exchange*:
* _Item_ - stores information about items on the site (who added, when, description, etc.). When these
are "deleted" from the main site, they remain in the database, but the boolean field "deleted" is set to 
false, and they won't show up on the list of all items (except in the admin page)
* _Notification_ - tracks notifications between users for an item, expire after a set period of time (currently 5 days, defined in exchange/models.py

###### Defined in built-in *contrib.auth*: 
* _User_ - stores passwords (as hashcodes), names, email, etc.

###### Defined in *admin_extension*: 
* _Profile_ - extends the User model, storing profile pictures, phone numbers and other information as needed
* _Info_ - stores the text of a few informational pages (about us and contact)

###### Defined in *stickies* :
* _Sticky_ - the stickies on the ask page, providing a discussion/bulletin board for things users are asking for.
As with Items, a user without staff priveleges cannot actually delete these from the database, only change their deleted field to False. 

The models for exchange, admin-extension and stickies are tracked through South, a Django app to assist
with database modifications and migrations. 

### Templates ###
Most of the templates are extensions of either base_items.html
or base_community.html, which are both extensions of base.html.

Internal links are formatted as {% url 'views.view_name' %}.

### Static Files ###
Static files (css and site images) are stored in the static directory
here for easy access and version control and symlinked to the public_html 
directory of the server, where django serves them from.User added images are 
stored in the media directory of public_html, but aren't tracked here.
These files are linked to in the templates with {{ STATIC_URL }}
and {{ MEDIA_URL }}.

Files used for server deplyment on a shared fcgi hosting environment
are backed up in the server directory.

Project to do:
--------------
- [x] users can log in and browse or add items
- [x] users can (optionally) add additional contact info or profile pitcures
- [x] items can be edited and deleted
- [x] notifications can be sent to indicate interest in an item
- [ ] update display of models in admin page
- [ ] add translation tags, can change language from admin page
- [x] move inline css to stylesheets
- [x] move common navigation elements to a base template
- [x] can add stickies
- [ ] stickies save upon leaving the text area (or clicking update)
- [ ] image thumbnail function (may be too difficult on shared hosting)
- [x] notifications expire after a deadline (5 days)
- [x] info pages (about, contact) editable from admin interface
- [ ] change display of notifications to be more visible and have no scrollbar
