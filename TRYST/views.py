from django.shortcuts import render, redirect, HttpResponse
from .models import RegistrationForm
from django.core.mail import send_mail , EmailMultiAlternatives
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.sessions.models import Session
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from email.mime.image import MIMEImage
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import random
import os
import django

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TRYST.settings")
django.setup()



# Create your views here.
def home(request):
    return render(request, "home.html")


def contact(request):
    firstname = request.POST.get("firstname", "")
    lastname = request.POST.get("lastname", "")
    usermail = request.POST.get("usremail", "")
    message = request.POST.get("description", "")

    from_email = "tryst24kmv@gmail.com"
    recipient_list = ["tryst24kmv@gmail.com"]
    subject = "New Query From TRYST Portal"
    message = f"Name: {firstname} {lastname}\nEmail ID: {usermail}\nQuery: {message}"
    if firstname and lastname and usermail and message:
        send_mail(subject, message, from_email, recipient_list)
        return redirect("contact")
    return render(request, "contact.html")


def events(request):
    return render(request, "events.html")

def generate_otp():
    otp = ''.join(random.choices('0123456789', k=6))
    return otp

def send_otp(request,receive_mail):
    otp = generate_otp()
    # request.session['otp'] = otp
    from_email = "tryst24kmv@gmail.com"
    recipient_list = [receive_mail]
    subject = "OTP Verification For TRYST Portal"
    message = f"Your One Time Password For Registration in TRYST Portal is: {otp}"

    send_mail(subject,message,from_email,recipient_list)

    return otp

def registration(request):
    name = request.POST.get("name", "")
    phone = request.POST.get("phone", "")
    email = request.POST.get("email", "")
    collegeName = request.POST.get("collegeName", "")
    image = request.FILES.get("image")

    if not (name and phone and email and collegeName and image):
        return render(request, "registration.html")
    

    if image:  # Make sure an image was uploaded
        # Define the directory where you want to save the image
        image_directory = os.path.join(settings.MEDIA_ROOT, 'images')
        os.makedirs(image_directory, exist_ok=True)

        filename = os.path.join(image_directory, f"{name[0:3]}_{phone}_{random.randint(100000,999999)}_img.png")

        with open(filename, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Store the path of the saved file in the session



    # d = RegistrationForm.objects.filter(email=email).values()
    # status = True
    # if len(d) != 0:
    #     status = False
    #     return render(request, "verification.html", {"status": status, "email": email})
    
    # session = SessionStore()
    request.session.create()
    request.session["name"] = name
    request.session["phone"] = phone
    request.session["email"] = email
    request.session["collegeName"] = collegeName
    # request.session["image"] = image
    request.session["image"] = filename
    
    otp = send_otp(request,email)

    request.session["otp"] = otp
    request.session.save()

    print(request.session.session_key)
    return render(request , "verification.html",{"status":True,"email":email})



def send_email(subject, message, receiver):
    subject = subject
    message = message
    from_email = EMAIL_HOST_USER
    recipient_list = [receiver]

    send_mail(subject, message, from_email, recipient_list)


def otp_verfication(request):
    # session_id = request.session.session_key
    session_id = request.session.session_key

    session_obj = Session.objects.get(session_key=session_id)
    session_data = session_obj.get_decoded()

    otp = session_data.get("otp")

    user_otp = request.POST.get("otp")

    if user_otp != otp:
        return render(request , "verification.html")
    
    elif user_otp == otp:
        user_name = session_data.get("name")
        user_phone = session_data.get("phone")
        user_email = session_data.get("email")
        user_collegeName = session_data.get("collegeName")
        user_idcard = session_data.get("image")
        uid = get_random_string(10,allowed_chars='0123456789zxcvbnm&%$#@')
        registration_data = RegistrationForm(name = user_name , phone = user_phone , collegeName = user_collegeName , email = user_email , StdIDCard = user_idcard,UID=uid)
        registration_data.save()

        # data = RegistrationForm.objects.get()
        # qr_code = data.Std_qr_code

        qr_code = registration_data.Std_qr_code

        html_content = render_to_string("email_body.html" , {'username' : user_name})
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives("TRYST'24 Entry Ticket" , text_content , EMAIL_HOST_USER , [user_email])
        email.attach_alternative(html_content , "text/html")
        email.attach_file(os.path.join(str(qr_code)))
        email.send()


        Session.objects.filter(session_key=session_id).delete()
        return render(request , "success.html")
    
    else:
        Session.objects.filter(session_key=session_id).delete()
        return render(request , "")
    

def viewprofile(request , link):
    if request.session["email"] in ["onlyforanshjuneja@gmail.com" , "shivmondal0132@gmail.com"]:
        # print(request)
        # print(link)
        data = RegistrationForm.objects.all()
        # for d in data:
        #     if d.email == 
        return render(request , "viewprofile.html")
    
    else:
        return HttpResponse("Unauthorised to access this page")

@login_required(login_url='viewadminpage')
def viewdata(request):
    uid = request.POST.get("uid",'')

    if not uid:
        return render(request,'userpage.html',{"status":False,"data":''})
    else:
        data = RegistrationForm.objects.all()
        print(data)
        userdata = ''
        for d in data:
            if d.UID == uid:
                userdata = d
                break
        print(userdata)
        return render(request,'userpage.html',{"status":True,"data":userdata})


def viewadminpage(request):
    adminname = request.POST.get("userid",'')
    adminpassword = request.POST.get("adminpassword",'')

    user = auth.authenticate(username=adminname, password=adminpassword)
    print(adminname)
    print(adminpassword)

    if user is not None:
        auth.login(request, user)
        return redirect('userdata')
    
    else:
        messages.info(request, "invalid credentials")
        return render(request , "viewadminpage.html")