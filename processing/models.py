# -*- coding: utf-8 -*-
from django.db import models
import subprocess
import threading
from django.conf import settings
from django.contrib.auth.models import User
from django import forms

#OPciones estáticas
POSIBLES_ESTADOS_PROCESOS = (
    (1, "Terminado exitosamente"),
    (0, "Terminado con errores"),
    (2, "Iniciado"),
    (3, "En espera")
    )
MAPEADORES = (
        (0, "BWA"),
        (1, "Bowtie"),
    )
# Create your models here.


class Proceso(models.Model):

    estado = models.IntegerField(choices=POSIBLES_ESTADOS_PROCESOS, default="3") 
    std_err = models.TextField(default="")
    std_out = models.TextField(default="")
    comando = models.CharField(max_length = 2000, default="echo Hola mundo")


    class Meta:
        verbose_name_plural = 'Procesos'


    def run_process(self):
        self.estado = 2
        self.save()
        try:
            p = subprocess.Popen(self.comando.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.std_out, self.std_err = p.communicate()
            self.estado = p.returncode
        except:
            try:
                self.std_out, self.std_err = p.communicate()
                self.estado = 0
                self.save()
            except:
                self.estado = 0
                self.save()
        self.save()


    def run(self):
        t = threading.Thread(target=self.run_process)
        t.setDaemon(True)
        t.start()


    def __unicode__(self):
        return u"ID: %s Estado: %s \n Comando: %s \n STDOUT: \n %s \n STDERR: %s\n " % (str(self.id), str(self.estado), str(self.comando), str(self.std_out), str(self.std_err))


class Mapeo(models.Model):
    in_left = []
    in_right = []

    proceso =  models.ForeignKey(Proceso)
    mapeador = models.IntegerField(choices=MAPEADORES) 

    class  Meta:
        verbose_name_plural = "Procesos de mapeo"



class ExpDiff(models.Model):
    sam_input = [ ]
 

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    #profile_pic = models.ImageField(upload_to='img/profile/%Y/%m/')

'''formulario para subir foto de perfil
class ImageUploadForm(forms.Form):
    image = forms.ImageField()
'''

class File(models.Model): 
    title = forms.CharField(max_length=50) 
    fileUpload = models.ImageField(upload_to='img/files/%Y/%m/') 
    description = models.CharField(max_length=200) 
    profile = models.ForeignKey(Profile) # formulario para subir cualquier archivo 
