from django.urls import path
from TRYST import views

urlpatterns = [
    path('' , views.home , name = 'home'),
]
