from django.urls import path
from .views import Register
urlpatterns = [
    path('',Register.as_view(),name="register"),

]
