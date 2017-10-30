from django.http import HttpResponse

def index(request):
    return HttpResponse('<b>Hello DCMPA</b>')