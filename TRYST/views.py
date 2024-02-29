<<<<<<< HEAD
from django.shortcuts import render,redirect,HttpResponse
from .models import ContactForm
=======
from django.shortcuts import render, redirect, HttpResponse
from .models import RegistrationForm
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD


>>>>>>> b6a570df02420777921a8fccab55259975563313
# Create your views here.
def home(request):
    return render(request, "home.html")


def contact(request):
<<<<<<< HEAD

    message = None
    clear_form = False

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        usremail = request.POST.get('usremail')
        description = request.POST.get('description')

        if not (firstname and lastname and usremail and description):
            message = 'Please fill out all fields.'
        else:
            contactdata = ContactForm(fname=firstname, lname=lastname, email=usremail, desc=description)
            contactdata.save()
            message = 'Thanks for contacting us! We will reach you soon...'
            clear_form = True

    return render(request, 'contact.html', {'message': message, 'clear_form': clear_form})



def events(request):
    return render(request , "events.html")
=======
    firstname = request.POST.get("firstname","")
    lastname = request.POST.get("lastname","")
    usermail = request.POST.get("usremail","")
    message = request.POST.get("description","")

    from_email = 'tryst24kmv@gmail.com'
    recipient_list = ['tryst24kmv@gmail.com']
    subject = "New Query From TRYST Portal"
    message = f'Name: {firstname} {lastname}\nEmail ID: {usermail}\nQuery: {message}'
    if firstname and lastname and usermail and message:
        send_mail(subject,message,from_email,recipient_list)
        return redirect("contact")
    return render(request, "contact.html")

def events(request):
    return render(request, "events.html")


def registration(request):
    name = request.POST.get("name", "")
    phone = request.POST.get("phone", "")
    dob = request.POST.get("dob", "")
    email = request.POST.get("email", "")
    collegeName = request.POST.get("collegeName", "")
    image = request.POST.get("image", "")

    if not (name and phone and dob and email and collegeName and image):
        return render(request, "registration.html")

    data = RegistrationForm.objects.all()
    for i in data:
        if i.email == email:
            print(i.email," Matched Found")
            # break

    registrationData = RegistrationForm(
        name=name,
        phone=phone,
        dob=dob,
        email=email,
        collegeName=collegeName,
        StdIDCard=image,
    )
    registrationData.save()
    return redirect("home")


def send_email(subject,message,receiver):
    subject = subject
    message = message
    from_email = EMAIL_HOST_USER
    recipient_list = [receiver]
    
    send_mail(subject , message , from_email , recipient_list)
>>>>>>> b6a570df02420777921a8fccab55259975563313
