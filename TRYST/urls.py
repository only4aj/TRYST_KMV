from django.urls import path
from TRYST import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('' , views.home , name = 'home'),
    path('contact/' , views.contact , name = 'contact'),
    path('events/' , views.events , name = "events"),
    path('registration/' , views.registration , name = "registration"),
    path('otp_verification/' , views.otp_verfication , name = "otp"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)