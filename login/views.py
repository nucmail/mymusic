from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout


from django.contrib.auth.models import User



class Login(View):
    def get(self,request):
        msg = False
        content ={
            msg : True,
            'error':"密码错误！"
        }
        messages.error(request,content['error'])
        return render(request,'login.html',content)

    def post(self,request):
        msg = False

        user_id = request.POST.get('user_id_login')
        user_password = request.POST.get('user_password_login')
        print('id',user_id)
        print('password',user_password)
        # request.user
        user = authenticate(request, username=user_id, password=user_password)

        #print('密文',User.objects.get(username=user_id).password)

        if (not (User.objects.filter(username=user_id).exists())):
            msg = True

            print('账户不存在')
            # return HttpResponseRedirect('login')
            return render(request, 'login.html', {
                'msg':msg,
                'error':'账号不存在！'
            })

        elif (check_password(user_password,User.objects.get(username=user_id).password)):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, '登录成功！')
            user = request.user
            print(user.username,'登录成功！')
            response = redirect("index")
            # 若登录成功，则设置cookie，加盐值可自己定义取，这里定义12小时后cookie过期
            response.set_signed_cookie("login", 'yes', salt="SSS", max_age=60 * 60 * 12)
            return response

        else:
            msg: True
            messages.error(request, '密码错误！')
            print('密码错误！')
            return render(request, 'login.html', {
                'msg':msg,
                'error':'密码错误！'})


    def logout(request):
        logout(request)
        print("退出成功！")
        # response = redirect(reverse('index'))
        # 退出登录时清除cookie中的username
        response = redirect('index')
        response.delete_cookie('username')
        return response

        # return render(request,'index')
