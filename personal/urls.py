from django.urls import path
from . import views
urlpatterns = [
    path('',views.personal,name = "personal_show"),
]
