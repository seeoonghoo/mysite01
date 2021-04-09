from django.http import HttpResponseRedirect
from django.shortcuts import render

from guestbook import models


def index(request):
    results = models.findall()
    data = {
        "guestbook_list": results
    }
    return render(request, 'guestbook/index.html', data)


def add(request):
    name = request.POST["name"]
    password = request.POST["password"]
    message = request.POST["message"]

    models.insert(name, password, message)

    return HttpResponseRedirect("/guestbook")


def deleteform(request):
    results = request.GET["no"]
    data = {"no": results}

    return render(request, 'guestbook/deleteform.html', data)


def delete(request):
    no = request.POST["no"]
    password = request.POST["password"]

    models.deleteby_no_and_password(no, password)

    return HttpResponseRedirect("/guestbook")