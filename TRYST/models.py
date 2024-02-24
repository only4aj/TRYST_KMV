from django.db import models

# Create your models here.
class ContactForm(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.CharField(max_length=5000)

    def __str__(self) -> str:
        return self.fname