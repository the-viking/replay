from django.utils import simplejson
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def flickr_save(request, new_title):
    dajax = Dajax()
    dajax.script('cancel_edit();')
    dajax.assign('#title', 'value', new_title)
    dajax.alert('Save complete using "%s"' % new_title)
    return dajax.json()