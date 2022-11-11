from django.urls import path
from . import views
urlpatterns = [
    path('',views.personal_edit.as_view(),name="personal_edit"),
]
