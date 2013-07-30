from django.http import Http404, HttpResponse

def item(request, id):
    html = "<html><body><p> Id is : " + id +  "</p></body></html>" 
    return HttpResponse(html)
