from django.urls import path
from index import views
urlpatterns = [
    path('',views.index.as_view(),name = "index"),
    path('index',views.index.as_view(),name = "index"),
    path('index_user',views.index_user.as_view()),
    path('index_music',views.index_music.as_view()),
    path('index_svd',views.index_svd.as_view()),
]
