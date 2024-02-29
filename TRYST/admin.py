from django.contrib import admin
from .models import ContactForm,RegistrationForm
# Register your models here.
admin.site.register(ContactForm)
admin.site.register(RegistrationForm)