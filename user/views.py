from django.http import HttpResponseRedirect
from django.shortcuts import render

from user import models


def joinform(request):
    return render(request, 'user/joinform.html')

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

def join(request):
    name = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]
    gender = request.POST["gender"]

    models.insert(name, email, password, gender)

    return HttpResponseRedirect('/user/joinsuccess.html')

def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):
    email = request.POST["email"]
    password = request.POST["password"]

    result = models.findby_email_and_password(email,password)
    if result is None:
        return HttpResponseRedirect('loginform?result=fail')


    # login 처리
    # csrftoken 으로 쿠키를 남겨놈. 얘는 계속 요청을 함. 그러니까 거기에 정보를 넣어놓으면 계속 돌아가니까 로그인? 대충 이런 느낌
    request.session["authuser"] = result # 'authuser' 라는 객체로 계속 요청을 해줌. 로그아웃은 이걸 없애는거

    return HttpResponseRedirect('/')

def logout(request):
    del request.session["authuser"]
    # 저기에 넣어놨던 정보를 지우니까 계속 요청을 해도 암것도 없으니까 로그아웃됨
    return HttpResponseRedirect('/')

def updateform(request):
    # Access Control(접근 제어)
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/')

    authuser = request.session["authuser"]
    result = models.findbyno(authuser["no"])

    data = {'data': result}

    return render(request, 'user/updateform.html',data)

def update(request):

    authuser = request.session["authuser"]
    no = authuser["no"]
    name = request.POST["name"]
    password = request.POST["password"]
    gender = request.POST["gender"]

    models.update(name,password,gender,no)

    result = models.findbyno(authuser["no"])
    request.session["authuser"] = result

    return HttpResponseRedirect('updateform')