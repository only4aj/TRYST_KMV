from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import random


# Create your models here.
class ContactForm(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.CharField(max_length=5000)

    def __str__(self) -> str:
        return self.fname


class RegistrationForm(models.Model):
    name = models.CharField(max_length=30)
    phone = models.PositiveBigIntegerField()
    collegeName = models.CharField(max_length=200)
    email = models.EmailField()
    course = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(default=0)
    StdIDCard = models.ImageField(upload_to="images")
    UID = models.CharField(max_length=7)
    otp = models.IntegerField(default=0)
    entryTime = models.IntegerField(default=0)
    Std_qr_code = models.ImageField(blank=True, upload_to="code")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        data = f"Student Name : {self.name}\nPhone Number : {self.phone}\nCollege Name : {self.collegeName}\nEmail : {self.email}\nCourse: {self.course}\nYear: {self.year}\nUNIQUE TRYST ID: {self.UID}\n\nVERIFIED USER"
        qr_image = qrcode.make(data)
        qr_offset = Image.new("RGB", (650, 650), "blue")
        qr_offset.paste(qr_image)
        files_name = f"{self.name}_{self.phone}_{random.randint(100000,999999)}.png"
        stream = BytesIO()
        qr_offset.save(stream, "PNG")
        self.Std_qr_code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)
