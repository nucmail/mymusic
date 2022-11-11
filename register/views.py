from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.models import User

from personal.models import user_fav
from personal.models import user_his
from personal.models import user_info

class Register(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        user_id = request.POST.get('user_id_register')
        user_password = request.POST.get('user_password_register')

        if(User.objects.filter(username=user_id).exists()):
            messages.error(request, '账号已经存在！')
            return render(request, 'login.html', {
                'msg': True,
                'error':"账号已经存在！"
            })


        elif user_password == '':
            return render(request,'register.html',{
                'register_msg':True,
                'error':'密码不能为空！'
            })
        else:
            messages.success(request,'注册成功！')

            userinfo = user_info.objects.create(user_id = user_id)
            userinfo.save()

            user = User.objects.create_user(username = user_id,password=user_password)
            user.save()
        # return HttpResponseRedirect('login')
        return render(request, 'login.html', {
            'register_msg': False,
        })

