from forms import *
from django.shortcuts import render
from processing.models import *
# Create your views here.

def upload_file(request): 
    if request.method == 'POST': 
        form = UploadFileForm(request.POST, request.FILES) 
        if form.is_valid(): 
            instance = File(fileUpload=request.FILES['file']) 
            instance.save() 
            return HttpResponseRedirect('/success/') 
    else: 
        form = UploadFileForm() 
        return render(request, 'upload.html', {'form': form})

############# AUTENTICATION ###############
def auth_view(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = authenticate(username=email,password=password)
    if user is not None:
        login(request, user)
        return render(request, 'home.html')
    else:
        return render(request, 'error_login.html')


def error_login(request):
    return render(request, 'error_login.html')


def log_in(request):
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    return render(request, 'logout.html')

############# REGISTRATION ###############
def register_user(request):
    if request.POST:
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password1', '')
        if password1 == password2:
            new_user = User(username=email,email=email)
            new_user.set_password(password1)
            new_user.save()
            new_profile = Profile(user=new_user,
                                  email=email,
                                  firstName=request.POST.get('firstName', ''),
                                  lastName=request.POST.get('lastName', ''),
                                  )
            new_profile.save()
            return render(request, 'registration_success.html')
        else:
            return render(request, 'registration_error.html')
    else:
        return render(request, 'register.html')


############# PAGE RENDER ###############
def home(request):
    return render(request, 'home.html')


def bowtie_form(request):
    return render(request, 'bowtie_form.html')


def bwa_form(request):
    return render(request, 'bwa_form.html')


def diffexp_form(request):
    return render(request, 'diffexp_form.html')

def upload_success(request):
    return render(request, 'upload_success.html')
