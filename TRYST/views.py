from django.shortcuts import render,redirect,HttpResponse
from .models import ContactForm
# Create your views here.
def home(request):
    return render(request , 'home.html')

def contact(request):

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