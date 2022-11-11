from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts  import render
from music.models import Song_store
from personal.models import user_his
import pandas as pd
from django.core.paginator import Paginator
from music.models import Song_store

class index(View):
    def get(self,request):
        from .recommend import popularity_recommender_py
        sys = popularity_recommender_py()
        songidlist = []
        useridlist = []
        plist = []
        fractional_play_countlist = []
        for item in user_his.objects.all():
            songidlist.append(item.song_id)
            useridlist.append(item.user_id)
            plist.append(item.p)
            fractional_play_countlist.append(item.fractional_play_count)
        df = pd.DataFrame({
            'song_id': songidlist,
            'user_id': useridlist,
            'p': plist,
            'fractional_play_count': fractional_play_countlist
        })
        sys = popularity_recommender_py()
        sys.create(df, "user_id", "song_id")
        songid_list = sys.recommend()
        song_list = Song_store.objects.filter(song_id__in=songid_list)

        #hot_list

        hot_list = user_his.objects.all().order_by('-fractional_play_count')[:10]
        print(hot_list.values())
        hot_res = []

        for item in hot_list:
            if Song_store.objects.filter(song_id=item.song_id).exists():
                hot_res.append({
                    'song_id': item.song_id,
                    'p': item.p,
                    'fractional_play_count':item.fractional_play_count,
                    'song_title': Song_store.objects.get(song_id=item.song_id).title,
                })

        #new_list

        new_list = Song_store.objects.all().order_by('-age')[:10]
        print(new_list.values())

        return render(request,'index.html', {
            'song_list': song_list,
            'hot_list':hot_res,
            'new_list': new_list,
        })

    def post(self,request):
        return render(request,'')

class index_music(View):

    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,'login.html')
        user = request.user
        user_id = user.username
        print(user_id)
        from .recommend import item_similarity_recommender_py
        sys = item_similarity_recommender_py()
        songidlist = []
        useridlist = []
        plist = []
        fractional_play_countlist = []
        for item in user_his.objects.all():
            songidlist.append(item.song_id)
            useridlist.append(item.user_id)
            plist.append(item.p)
            fractional_play_countlist.append(item.fractional_play_count)
        df = pd.DataFrame({
            'song_id': songidlist,
            'user_id': useridlist,
            'p': plist,
            'fractional_play_count': fractional_play_countlist
        })
        sys.create(df, user_id="user_id", item_id="song_id")
        songid_list = sys.recommend(user_id)
        song_list = Song_store.objects.filter(song_id__in=songid_list)

        #hot_list

        hot_list = user_his.objects.all().order_by('-fractional_play_count')[:10]
        print(hot_list.values())
        hot_res = []

        for item in hot_list:
            if Song_store.objects.filter(song_id=item.song_id).exists():
                hot_res.append({
                    'song_id': item.song_id,
                    'p': item.p,
                    'fractional_play_count':item.fractional_play_count,
                    'song_title': Song_store.objects.get(song_id=item.song_id).title,
                })

        #new_list

        new_list = Song_store.objects.all().order_by('-age')[:10]
        print(new_list.values())

        return render(request,'index_music.html', {
            'song_list': song_list,
            'hot_list':hot_res,
            'new_list': new_list,
        })

    def post(self,request):
        return render(request,'')

class index_user(View):

    def get(self,request):
        # 获取当前用户的id，默认值
        if not request.user.is_authenticated:
            return render(request,'login.html')
        user = request.user
        user_id = user.username

        print(user_id)
        from .recommend import user_similarity_recommender_py
        sys = user_similarity_recommender_py()
        songidlist = []
        useridlist = []
        plist = []
        fractional_play_countlist = []
        for item in user_his.objects.all():
            songidlist.append(item.song_id)
            useridlist.append(item.user_id)
            plist.append(item.p)
            fractional_play_countlist.append(item.fractional_play_count)
        df = pd.DataFrame({
            'song_id': songidlist,
            'user_id': useridlist,

            'p': plist,
            'fractional_play_count': fractional_play_countlist
        })
        sys.create(df, "user_id", "song_id", user_id)
        songid_list = sys.get_ans()
        song_list = Song_store.objects.filter(song_id__in=songid_list)
        #hot_list

        hot_list = user_his.objects.all().order_by('-fractional_play_count')[:10]
        print(hot_list.values())
        hot_res = []

        for item in hot_list:
            if Song_store.objects.filter(song_id=item.song_id).exists():
                hot_res.append({
                    'song_id': item.song_id,
                    'p': item.p,
                    'fractional_play_count':item.fractional_play_count,
                    'song_title': Song_store.objects.get(song_id=item.song_id).title,
                })

        #new_list

        new_list = Song_store.objects.all().order_by('-age')[:10]
        print(new_list.values())

        return render(request,'index_user.html', {
            'song_list': song_list,
            'hot_list':hot_res,
            'new_list': new_list,
        })


    def post(self,request):
        return render(request,'')

class index_svd(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,'login.html')
        user = request.user
        user_id = user.username
        print(user_id)
        from .recommend import SVD
        sys = SVD()
        songidlist = []
        useridlist = []
        plist = []
        fractional_play_countlist = []
        for item in user_his.objects.all():
            songidlist.append(item.song_id)
            useridlist.append(item.user_id)
            plist.append(item.p)
            fractional_play_countlist.append(item.fractional_play_count)
        df = pd.DataFrame({
            'song_id': songidlist,
            'user_id': useridlist,
            'p': plist,
            'fractional_play_count': fractional_play_countlist
        })
        sys.create(df, user_id)
        songid_list = sys.get_ans()
        song_list = Song_store.objects.filter(song_id__in=songid_list)


        #hot_list

        hot_list = user_his.objects.all().order_by('-fractional_play_count')[:10]
        print(hot_list.values())
        hot_res = []

        for item in hot_list:
            if Song_store.objects.filter(song_id=item.song_id).exists():
                hot_res.append({
                    'song_id': item.song_id,
                    'p': item.p,
                    'fractional_play_count':item.fractional_play_count,
                    'song_title': Song_store.objects.get(song_id=item.song_id).title,
                })

        #new_list

        new_list = Song_store.objects.all().order_by('-age')[:10]
        print(new_list.values())

        return render(request,'index_svd.html', {
            'song_list': song_list,
            'hot_list':hot_res,
            'new_list': new_list,
        })

    def post(self,request):
        return render(request,'')














