#!/home3/replaypr/python27/bin/python27
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/home3/replaypr/python27")
sys.path.insert(13, "/home3/replaypr/play")
sys.path.insert(0, "/home3/replaypr/.local/lib/python2.6/site-packages/django")

os.environ['DJANGO_SETTINGS_MODULE'] = 'play.settings'
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
