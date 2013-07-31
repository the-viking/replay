replay
======
A technology probe built and designed by Maria Håkansson, Erik Bonadonna and Jung-Hu Sohn, 
out of the Information Science department of Cornell University in summer of 2013.

Replay is meant to explore notions of necessity and people' feelings about what things
they really need and make them happy.

Replay is implemented as a Django application, with the models defined
in the exchange app (exchange/models.py), project settings in play/settings.py, 
view controller functions in play/views.py, and html templates in
the templates directory.

Models (Profiles, Users, Items and Notifications)
are stored in a MySQL database.

Static files (css and site images) and user added images are stored
in the public_html directory of our blue host server, and are not 
tracked here.

Files used for server deplyment on a shared fcgi hosting environment
are backed up in the server directory.

Project checklist:
- [x] users can log in and browse or add items
- [x] users can (optionally) add additional contact info or profile pitcures
- [x] items can be edited and deleted
- [ ] notifications can be sent to indicate interest in an item
