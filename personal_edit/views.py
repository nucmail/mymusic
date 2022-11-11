from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
# Create your views here.
from django.views import View

from music.models import Song_store
from personal.models import user_info, user_fav, user_his


class personal_edit(View):
    def get(self,request):
        user = request.user
        print(type(user.username))
        fav_list = user_fav.objects.filter(user_id=user.username)
        print(fav_list.values())

        his_list = user_his.objects.filter(user_id=user.username)
        print(his_list.values())

        fav_res = []

        for item in fav_list:
            if Song_store.objects.filter(song_id=item.song_id).exists():
                fav_res.append({
                    'song_id': item.song_id,
                    'song_title': Song_store.objects.get(song_id=item.song_id).title,
                })
        his_list = user_his.objects.filter(user_id=user.username)

        his_res = []

        for item in his_list:
            if Song_store.objects.filter(song_id=item.song_id).exists():
                his_res.append({
                    'song_id': item.song_id,
                    'p': item.p,
                    'song_title': Song_store.objects.get(song_id=item.song_id).title,
                })

        try:
            page = int(request.GET.get('page', 1))
            if page < 1:
                print("-----", page)
                page = 1
        except Exception:
            print("----")
            page = 1
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

        # return render(request, 'personal_edit.html',
        # {'fav_list':fav_list,
        #  'his_list':his_list,
        #  'user_name':user_info.objects.get(user_id = user.username).user_name,
        # 'user_email':user_info.objects.get(user_id = user.username).user_email,
        # 'user_phone':user_info.objects.get(user_id = user.username).user_phone,})
        return render(request, "personal_edit.html", {
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

    def post(self,request):
        register_msg = False
        user = request.user
        print(user.username)
        user_name = request.POST.get('edit_name')
        user_email = request.POST.get('edit_email')
        user_phone = request.POST.get('edit_phone')
        user_password = request.POST.get('edit_password')
        print(user_password)
        print(type(user_password))
        if user_password == '':
            register_msg = True
            error = "密码不能为空！"
            print(error)
            fav_list = user_fav.objects.filter(user_id=user.username)
            print(fav_list.values())

            his_list = user_his.objects.filter(user_id=user.username)
            print(his_list.values())
            return render(request, 'personal_edit.html',
                          {'fav_list': fav_list,
                           'his_list': his_list,
                           'user_name': user_info.objects.get(user_id=user.username).user_name,
                           'user_email': user_info.objects.get(user_id=user.username).user_email,
                           'user_phone': user_info.objects.get(user_id=user.username).user_phone,
                           'register_msg' : register_msg,
                            'error' : error,
                           })



        print(user_name)

        User.objects.filter(username=user.username).update(
            password=make_password(user_password),
            email=user_email,
        )

        user_info.objects.filter(user_id=user.username).update(
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
        )

        return render(request,'login.html',{
            'register_msg':True,
            'error':'修改成功！',
            'register_msg':register_msg
        })
    # return HttpResponseRedirect('personal_show')
