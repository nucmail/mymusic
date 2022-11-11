import os

from django.db import models
from django.utils import timezone #引入timezone
# Create your models here.
# def user_directory_path(instance, filename):
#     ext = filename.split('.').pop()
#     filename = '{0}{1}.{2}'.format(instance.name, instance.identity_card, ext)
#     return os.path.join(instance.major.name, filename) # 系统路径分隔符差异，增强代码重用性


#
# class User(models.Model):#类名即为表名
#
#     id = models.CharField('User_ID',primary_key=True,max_length=15)
#     name = models.CharField('User_NAME',max_length=20,default = "")
#     email = models.EmailField('user_email',blank=True,default="")
#     password = models.CharField(max_length=10,blank=False,default='123456')

#     last_login = models.DateTimeField(default='0000-00-00 00:00:00', blank=True, null=True)
    # img = models.ImageField()
    #
    # # upload_to 参数接收一个回调函数 user_directory_path，该函数返回具体的路径字符串，图片会自动上传到指定路径下，即 MEDIA_ROOT + upload_to
    # # user_directory_path 函数必须接收 instace 和 filename 两个参数。参数 instace 代表一个定义了 ImageField 的模型的实例，说白了就是当前数据记录；filename 是原本的文件名
    # # null 是针对数据库而言，如果 null = True, 表示数据库的该字段可以为空；blank 是针对表单的，如果 blank = True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响
    #
    # # 这里定义一个方法，作用是当用户注册时没有上传照片，模板中调用 [ModelName].[ImageFieldName].url 时赋予一个默认路径
    #
    # def photo_url(self):
    #     if self.photo and hasattr(self.photo, 'url'):
    #         return self.photo.url
    #     else:
    #         return '/media/default/user.jpg'