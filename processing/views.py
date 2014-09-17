from forms import *
from processing.models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template import loader, Context, RequestContext
from django.contrib.auth import authenticate, login, logout
import os
# Create your views here.



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



############# File Upload ###############

@login_required(login_url='/login/')
def filesubmit(request): 
    if request.method == 'POST':
        #try:
        desc = request.POST.get('description', '')
        user = User.objects.select_related().get(id=request.user.pk)
        p = user.profile
        instance = File(fileUpload=request.FILES['file'],description=desc,profile=p)
        instance.save() 
        return HttpResponseRedirect('/files/success/') 
        #except Exception as e:
        #    print e
    else:
        return render(request, 'upload.html')

############# PAGE RENDER ###############
def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
def bowtie_form(request):
    return render(request, 'bowtie_form.html')


@login_required(login_url='/login/')
def bwa_form(request):
    return render(request, 'bwa_form.html')


@login_required(login_url='/login/')
def diffexp_form(request):
    return render(request, 'diffexp_form.html')


@login_required(login_url='/login/')
def upload_success(request):
    return render(request, 'upload_success.html')


@login_required(login_url='/login/')
def show_files(request):
    user = User.objects.select_related().get(id=request.user.pk)
    profile = user.profile
    file_list = profile.file_set.all()
    return render(request, 'files.html',{'file_list':file_list})



@login_required(login_url='/login/')
def show_fileupload(request):
    form = UploadFileForm()
    return render(request, 'fileupload.html',{'form':form})
