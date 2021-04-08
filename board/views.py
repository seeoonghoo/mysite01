from math import ceil

from django.shortcuts import render
from django.http import HttpResponseRedirect

from board import models

LIST_COUNT = 10 #한 페이지당 게시글 10개

def index(request):
    page = request.GET.get("p")
    if page is None:
        page = 1
    elif str(page).isalpha():
        return HttpResponseRedirect('/')
    else:
        page = int(page)

    totalcount = models.count() #게시글 총 개수
    boardlist = models.findall(page, LIST_COUNT)

    # paging 정보를 계산

    # 총 페이지가 나와야 할 개수
    pagecount = ceil(totalcount["count(*)"]/LIST_COUNT)
    
    tmp = []
    pageindex = page // 5
    for i in range(5):
        tmp.append((5 * pageindex) + i + 1)

    tmpmin=min(tmp) # 이전페이지 계산용
    tmpmax=max(tmp) # 다음페이지 계산용
    contentstotal = totalcount["count(*)"]

    if page == 1:
        maxindex = totalcount["count(*)"]
    else:
        maxindex = totalcount["count(*)"] - (page-1) * 10

    if 'authuser' not in request.session:
        result = {"no" : 0}
    else:
        authuser = request.session["authuser"]
        result = models.findbyno(authuser["no"])
        
    # 여기서부터는 이제 depth에 따라 들어가게 함


    
    data = {
        "boardlist" : boardlist, #정보들 거의 다 넘김 삭제 x
        "correctpage" : page, # 현재 페이지 삭제 x
        "totalcount" : contentstotal, #게시글 인덱싱 해줄거 삭제 x
        "numberlist" : tmp, # 페이지 인덱스리스트 삭제 x
        "pagecount" : pagecount, # 총페이지개수, 삭제 x
        "minnumberlist" : tmpmin, # 이전페이지 계산용 삭제 x
        "maxnumberlist" : tmpmax, # 다음페이지 계산용 삭제 x
        "presentmaxindex" : maxindex, # 현재 페이지 게시글의 가장 큰 인덱스 삭제 x
        "authuser" : result # 현재 로그인 하고 있는 사람
    }

    return render(request,'board/index.html',data)

def view(request):

    no = request.GET.get("no")
    if no is None:
        no = 1
    elif str(no).isalpha():
        return HttpResponseRedirect('/')
    else:
        no = int(no)

    models.hit_update(no)
    result = models.view_findbyno(no)

    if 'authuser' not in request.session:
        authresult = {"no" : 0}
    else:
        authuser = request.session["authuser"]
        authresult = models.findbyno(authuser["no"])
    page = request.GET.get("p")
    data = { "viewlist" : result,
             "authuser" : authresult,
             "no" : no,
             "page" : page}

    return render(request,'board/view.html', data)


def writeform(request):

    # Access Control(접근 제어)
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/')

    authuser = request.session["authuser"]
    result = models.findbyno(authuser["no"])

    data = {'data': result}

    return render(request, 'board/writeform.html',data)

def write(request):

    authuser = request.session["authuser"]
    no = authuser["no"]
    title = request.POST["title"]
    contents = request.POST["contents"]

    models.write(no,title,contents)

    return HttpResponseRedirect('/board')


def deleteform(request):
    no = request.GET.get("no")
    if no is None:
        no = 1
    elif str(no).isalpha():
        return HttpResponseRedirect('/')
    else:
        no = int(no)

    if 'authuser' not in request.session:
        return HttpResponseRedirect('/')

    authuser = request.session["authuser"]
    result = models.findbyno(authuser["no"])

    board_user_num = models.real_findbyno(no)

    if result["no"] != board_user_num["user_no"]:
        return HttpResponseRedirect("/board")

    data = {"no": no}

    return render(request, 'board/deleteform.html', data)


def delete(request):
    no = request.POST["no"]

    models.deleteby_no(no)

    return HttpResponseRedirect("/board")

def updateform(request):
    # Access Control(접근 제어)

    no = request.GET.get("no")
    if no is None:
        no = 1
    elif str(no).isalpha():
        return HttpResponseRedirect('/')
    else:
        no = int(no)

    if 'authuser' not in request.session:
        return HttpResponseRedirect('/')

    authuser = request.session["authuser"]
    result = models.findbyno(authuser["no"])

    board_user_num = models.real_findbyno(no)

    if authuser["no"] != board_user_num["user_no"]:
        return HttpResponseRedirect("/board")


    updateinfo = models.update_findbyno(no)

    data = {"no": no,
            "updatelist": updateinfo}

    return render(request, 'board/updateform.html',data) #절대절대절대 지우지 말것 data 갖고 가야함

def update(request):

    no = request.POST["no"]
    title = request.POST["title"]
    contents = request.POST["contents"]

    models.updateby_no(title,contents,no)

    return HttpResponseRedirect(f'/board/view?no={no}')

def replyform(request):

    # Access Control(접근 제어)
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/')

    authuser = request.session["authuser"]
    result = models.findbyno(authuser["no"])

    no = request.GET.get("no")
    if no is None:
        no = 1
    elif str(no).isalpha():
        return HttpResponseRedirect('/')
    else:
        no = int(no)

    data = {"no" : no}

    return render(request, 'board/replyform.html',data)

def reply(request):

    authuser = request.session["authuser"]
    no = authuser["no"]
    title = request.POST["title"]
    contents = request.POST["contents"]

    postnum = request.POST["no"]
    print(postnum, "============================")
    additional = models.reply_findall(postnum)
    print(additional, "=========================================")
    g_no = additional["g_no"]
    o_no = additional["o_no"] + 1
    depth = additional["depth"] + 1
    models.reply(no,title,contents, g_no, o_no, depth)

    return HttpResponseRedirect('/board')

def search(request):
    page = request.GET.get("p")
    if page is None:
        page = 1
    elif str(page).isalpha():
        return HttpResponseRedirect('/')
    else:
        page = int(page)

    keyword = request.POST["kwd"]

    # keyword 넣어서 제목에 그게 있는지 확인하고
    # 해당되는 애들을 전체 가져오고
    # 그거의 카운트를 구해서 아래꺼에 대신 넣으면 끝
    boardlist = models.search_find(keyword,page,LIST_COUNT)
    print(len(boardlist), "==================")


    totalcount = len(boardlist) # 게시글 총 개수


    # paging 정보를 계산

    # 총 페이지가 나와야 할 개수
    pagecount = ceil(totalcount / LIST_COUNT)

    tmp = []
    pageindex = page // 5
    for i in range(5):
        tmp.append((5 * pageindex) + i + 1)

    tmpmin = min(tmp)  # 이전페이지 계산용
    tmpmax = max(tmp)  # 다음페이지 계산용
    contentstotal = totalcount

    if page == 1:
        maxindex = totalcount
    else:
        maxindex = totalcount - (page - 1) * 10

    if 'authuser' not in request.session:
        result = {"no": 0}
    else:
        authuser = request.session["authuser"]
        result = models.findbyno(authuser["no"])

    # 여기서부터는 이제 depth에 따라 들어가게 함

    data = {
        "boardlist": boardlist,  # 정보들 거의 다 넘김 삭제 x
        "correctpage": page,  # 현재 페이지 삭제 x
        "totalcount": contentstotal,  # 게시글 인덱싱 해줄거 삭제 x
        "numberlist": tmp,  # 페이지 인덱스리스트 삭제 x
        "pagecount": pagecount,  # 총페이지개수, 삭제 x
        "minnumberlist": tmpmin,  # 이전페이지 계산용 삭제 x
        "maxnumberlist": tmpmax,  # 다음페이지 계산용 삭제 x
        "presentmaxindex": maxindex,  # 현재 페이지 게시글의 가장 큰 인덱스 삭제 x
        "authuser": result  # 현재 로그인 하고 있는 사람
    }

    return render(request, 'board/search.html', data)
