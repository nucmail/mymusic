import pymysql
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import user_fav
from .models import user_his
from .models import user_info
from music.models import Song_store
from django.contrib.auth.models import User
from django.views.generic import View
# Create your views here.


def personal(request):

    user = request.user
    print('当前登录的用户为：'+user.username)
    ######################            收藏            #################################
    # 收藏，需要歌曲ID，歌曲名（用Song_sotre,user_fav）

    fav_list = user_fav.objects.filter(user_id=user.username)
    print(fav_list.values())
    fav_res = []

    for item in fav_list:
        if Song_store.objects.filter(song_id=item.song_id).exists():
            fav_res.append({
                'song_id': item.song_id,
                'song_title': Song_store.objects.get(song_id=item.song_id).title,
            })


######################       评分       #################################
    #评分记录，需要歌曲ID，歌曲名，评分,用(Song_sotre(歌曲名),user_his（用户ID筛选，拿歌曲ID，评分））

    try:
        page = int(request.GET.get('page',1))
        if page<1:
            print("-----",page)
            page = 1
    except Exception:
        print("----")
        page = 1

    his_list = user_his.objects.filter(user_id=user.username )


    his_res = []

    for item in his_list:
        if Song_store.objects.filter(song_id=item.song_id).exists():
            his_res.append({
                'song_id':item.song_id,
                'p':item.p,
                'song_title':Song_store.objects.get(song_id=item.song_id).title,
            })


    paginator = Paginator(his_res, 20)
    page_song_list = paginator.page(page)
    print(type(page_song_list))
    print(page_song_list)



    page_num = paginator.num_pages

    if page_song_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_song_list.has_previous():
        pre_page = page - 1
    else:
        pre_page = page - 1


    return render(request, "personal_show.html", {
        'user_name': user_info.objects.get(user_id=user.username).user_name,
        'user_email': user_info.objects.get(user_id=user.username).user_email,
        'user_phone': user_info.objects.get(user_id=user.username).user_phone,
        'fav_list': fav_res,
        'his_list': page_song_list,
        "cur_page": page,
        "page_num": range(page, min(page_num + 1, page + 5)),
        "pre_page": pre_page,
        "next_page": next_page
    })
