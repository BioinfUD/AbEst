# -*- coding: utf-8 -*-

from django.db import models
import subprocess
import threading
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from time import sleep
from django.core.files import File as Django_File
from django.conf import settings




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
TIPOS_MAPEO = (
        (0, "Single end"),
        (1, "Paired end")
    )
# Create your models here.


class Proceso(models.Model):

    estado = models.IntegerField(choices=POSIBLES_ESTADOS_PROCESOS, default=3) 
    std_err = models.TextField(default="")
    std_out = models.TextField(default="")
    comando = models.CharField(max_length = 2000, default="echo Hola mundo")

    class Meta:
        verbose_name_plural = 'Procesos'


    def run_process(self):
        self.estado = 2
        self.save()
        try:
            p = subprocess.Popen(str(self.comando).split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    #profile_pic = models.ImageField(upload_to='img/profile/%Y/%m/')
    def __unicode__(self):
        return unicode(self.email)

class File(models.Model): 
    fileUpload = models.FileField() 
    description = models.TextField(default="") 
    profile = models.ForeignKey(Profile) # formulario para subir cualquier archivo 
    def __unicode__(self):
        return unicode(self.description)

class Mapeo(models.Model):
    name = models.TextField(default="Experimento")
    procesos =  models.ManyToManyField(Proceso)
    mapeador = models.IntegerField(choices=MAPEADORES, default=1) 
    tipo = models.IntegerField(default=1, choices=TIPOS_MAPEO)
    profile = models.ForeignKey(Profile) 
    out_file = models.ForeignKey(File, null=True)

    def run_bowtie(self, reference, reads_1="", reads_2="", reads_se="",type=1):
        reference_file = reference #Full path
        reference_path = reference_file[::-1].split(" ",2)[1][::-1]
        reference_index = reference_path + "/" + reference_file.split("/")[-1].replace(" ","_").replace(".fasta", "").replace(".fa", "")
        comando = "bowtie-build %s %s" % (reference_index, reference_file)
        p1 = Proceso(comando=comando)
        p1.save()
        self.procesos.add(p1)
        #To get files with path trin.fileUpload.path
        #Genero indice y espero hasta que este listo
        t1 = threading.Thread(target=p1.run_process)
        t1.setDaemon(True)
        t1.start()
        while t1.isAlive():
            sleep(1)
        file_name = "/tmp/%s.bam" % self.name.replace(" ", "_") 
        if self.tipo==1:
            mates1 = "','.join(reads_1)"
            mates2 = "','.join(reads_2)"
            #out_bam = "%s.bam" % self.name.replace(" ", "_")
            comando = "bowtie -p %s  %s -1 %s -2 %s  - > %s | samtools view -bSh - > %s " % (settings.CORES, reference_index, mates1, mates2, file_name)
        elif self.tipo==0:
            mates=","join(reads_se)
            comando = "bowtie -p %s  %s -s %s   - > %s | samtools view -bSh - > %s " % (settings.CORES, reference_index, mates, file_name)
        p2 = Proceso(comando=str(comando))
        p2.save()
        self.procesos.add(p2)
        t2 = threading.Thread(target = p2.run_process)
        t2.setDaemon(True)
        t2.start()
        while t2.isAlive():
            sleep(1)
        self.save()
        out_file = File(fileUpload=Django_File(open(file_name)), description="Salida "+ self.name, profile=self.profile)
        out_file.save()
        self.out_file = out_file


    def run(self):
        self.name = "Experimento %s" % self.id
        self.save()
        if self.mapeador==1:
            t = threading.Thread(target=self.run_bowtie)
        elif self.mapeador==2:
            t = threading.Thread(target=self.run_bowtie) # Replace for bwa when ready
        t.setDaemon(True)
        t.run()



    class  Meta:
        verbose_name_plural = "Procesos de mapeo"



class ExpDiff(models.Model):
    sam_input = [ ]


"""

formulario para subir foto de perfil
class ImageUploadForm(forms.Form):
    image = forms.ImageField()
"""