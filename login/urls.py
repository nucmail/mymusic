
from django.urls import path
from .views import Login
#sfrom .views import  Logout
urlpatterns = [
    path('', Login.as_view(), name ="login"),
    path('logout/', Login.logout, name ="logout"),
]

