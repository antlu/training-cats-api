from django.http import HttpResponse
from django.shortcuts import render


def ping(request):
    return HttpResponse("Cats Service. Version 0.1", content_type='text/plain')
