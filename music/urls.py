
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.show_song),
    path('', views.show_song,name = "music"),
]

