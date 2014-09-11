from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    #profile_pic = models.ImageField(upload_to='img/profile/%Y/%m/')

# archivo con el perfi al que pertenece
class File(models.Model):
    title = forms.CharField(max_length=50)
    #fileUpload = models.ImageField(upload_to='img/files/%Y/%m/')
    description = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile)

'''formulario para subir foto de perfil
class ImageUploadForm(forms.Form):
    image = forms.ImageField()
'''
# formulario para subir cualquier archivo
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    fileUploaded = forms.FileField()
    description = models.CharField(max_length=200)