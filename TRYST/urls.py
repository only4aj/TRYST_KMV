from django.urls import path
from TRYST import views

urlpatterns = [
    path('' , views.home , name = 'home'),
    path('contact/' , views.contact , name = 'contact'),
    path('events/' , views.events , name = "events"),
]
