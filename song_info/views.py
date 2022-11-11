from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from music.models import Song_store
from personal.models import user_fav
from personal.models import user_his
from .models import song_his_temp
from .models import song_rivew


def show_info(request):


    songid = request.GET.get('songid',"")
    song_his_temp.objects.create(song_id=songid)
    print(songid)
    user = request.user
    if user_his.objects.filter(Q(song_id=songid) & Q(user_id=user.username)).exists():
        last_score = user_his.objects.get(Q(song_id=songid) & Q(user_id=user.username))
    else:
        last_score = 0

    songinfo = Song_store.objects.filter(song_id=songid)
    print(songinfo.values())

    #拿到评分
    song_review = song_rivew.objects.filter(song_id=songid)


    if user_fav.objects.filter(Q(song_id=songid) & Q(user_id=user.username)).exists():

        return render(request, "song_info.html", {
            'songinfo': songinfo,
            'like_flag': True,
            'last_score':last_score,
            'song_review':song_review,
        })
    else:
        return render(request, "song_info.html", {
            'songinfo': songinfo,
            'like_flag': False,
            'last_score': last_score,
            'song_review': song_review,
        })


class score(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return render(request,'login.html')
        songid = song_his_temp.objects.last().song_id

        print(songid)
        user = request.user

        #songinfo = user_his.objects.filter(Q(song_id=songid) & Q(user_id=user.username))
        score_input = request.POST.get('score_input')
        print(score_input)

        songinfo = Song_store.objects.filter(song_id=songid)
        #判断有无记录，有则改，无则添加
        if user_his.objects.filter(Q(user_id=user.username)&Q(song_id=songid)).exists():
            #存在
            print("yes")
            user_his.objects.filter(Q(song_id=songid)&Q(user_id=user.username)).update(p = score_input)
        else:
            user_his.objects.create(song_id=songid,user_id=user.username,p = score_input)

        if user_his.objects.filter(Q(song_id=songid) & Q(user_id=user.username)).exists():
            last_score = user_his.objects.get(Q(song_id=songid) & Q(user_id=user.username))
        else:
            last_score = 0

        # 拿到评分
        song_review = song_rivew.objects.filter(song_id=songid)


        if user_fav.objects.filter(Q(song_id=songid) & Q(user_id=user.username)).exists():

            return render(request, "song_info.html", {
                'songinfo': songinfo,
                'like_flag': True,
                'last_score':last_score,
                'song_review': song_review,
            })
        else:
            return render(request, "song_info.html", {
                'songinfo': songinfo,
                'like_flag': False,
                'last_score': last_score,
                'song_review': song_review,
            })

class Like(View):
    def post(self,request):
        #如果查到了，那就删除
        #如果查不到，那就添加
        print("start")
        if not request.user.is_authenticated:
            return render(request,'login.html')
        user = request.user
        songid = song_his_temp.objects.last().song_id
        print(songid)
        if user_fav.objects.filter(Q(song_id=songid)&Q(user_id=user.username)).exists():

            user_fav.objects.filter(Q(song_id=songid)&Q(user_id=user.username)).delete()
        else:
            #不存在，则添加
            user_fav.objects.create(song_id=songid,user_id=user.username)


        songinfo = Song_store.objects.filter(song_id=songid)
        #返回当前界面

        if user_his.objects.filter(Q(song_id=songid) & Q(user_id=user.username)).exists():
            last_score = user_his.objects.get(Q(song_id=songid) & Q(user_id=user.username))
        else:
            last_score = 0

        # 拿到评分
        song_review = song_rivew.objects.filter(song_id=songid)


        if user_fav.objects.filter(Q(song_id=songid) & Q(user_id=user.username)).exists():

            return render(request, "song_info.html", {
                'songinfo': songinfo,
                'like_flag': True,
                'last_score':last_score,
                'song_review': song_review,
            })
        else:
            return render(request, "song_info.html", {
                'songinfo': songinfo,
                'like_flag': False,
                'last_score': last_score,
                'song_review': song_review,
            })


#评分
class Review(View):
    def post(self,request):

        print("start")
        if not request.user.is_authenticated:
            return render(request,'login.html')
        user = request.user
        songid = song_his_temp.objects.last().song_id
        print(songid)

        #拿数据，存数据库
        review_text = request.POST.get('song_review_content')
        song_rivew.objects.create(song_id=songid,user_id=user.username, review= review_text)

        songinfo = Song_store.objects.filter(song_id=songid)
        #返回当前界面
        if user_his.objects.filter(Q(song_id=songid) & Q(user_id=user.username)).exists():
            last_score = user_his.objects.get(Q(song_id=songid) & Q(user_id=user.username))
        else:
            last_score = 0

        # 拿到评分
        song_review = song_rivew.objects.filter(song_id=songid)


        if user_fav.objects.filter(Q(song_id=songid) & Q(user_id=user.username)).exists():

            return render(request, "song_info.html", {
                'songinfo': songinfo,
                'like_flag': True,
                'last_score':last_score,
                'song_review': song_review,
            })
        else:
            return render(request, "song_info.html", {
                'songinfo': songinfo,
                'like_flag': False,
                'last_score': last_score,
                'song_review': song_review,
            })