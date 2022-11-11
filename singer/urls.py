
from django.urls import path
from . import views
urlpatterns = [
    path('', views.singer,name = "singer"),

]
