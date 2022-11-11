from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import search as search_his
from django.views.generic import View
from music.models import Song_store



def search(request):
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            print("页码错误！", page)
            page = 1
    except Exception:
        print("----")
        page = 1


    if(request.GET.get('search_text')):
        search_text = request.GET.get('search_text')
        search_his.objects.create(search_his = search_text)


    else:
        search_text = search_his.objects.last().search_his
    print("text:"+search_text)

    search_list = Song_store.objects.filter(title__icontains=search_text)

    paginator = Paginator(search_list, 20)
    page_song_list = paginator.page(page)
    page_num = paginator.num_pages

    if page_song_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_song_list.has_previous():
        pre_page = page - 1
    else:
        pre_page = page - 1



    if not Song_store.objects.filter(title__icontains=search_text).exists():

        error = "没有找到歌曲！"
        print(error)
        messages.error(request,error)
        return render(request, "search.html", {
            "songlist": page_song_list,
            "cur_page": page,
            "page_num": range(page, min(page_num + 1, page + 5)),
            "pre_page": pre_page,
            "next_page": next_page,
            'search_list': search_list,
            'search_msg': True,
            'messages': messages,
        })
    return render(request, "search.html", {
        "songlist": page_song_list,
        "cur_page": page,
        "page_num": range(page, min(page_num + 1, page + 5)),
        "pre_page": pre_page,
        "next_page": next_page,
        'search_list':search_list,
        'search_msg':False,
        'messages':messages,
    })


