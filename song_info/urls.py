
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_info,name = "song_info"),
    path('score_submit/', views.score.as_view(),name = "score_submit"),
    path('like_submit/', views.Like.as_view(),name = "like_submit"),
    path('review_submit/', views.Review.as_view(), name="review_submit"),
]

