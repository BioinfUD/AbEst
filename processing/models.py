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
from random import randint

# Opciones estáticas
POSIBLES_ESTADOS_PROCESOS = (
    (0, "Terminado exitosamente"),
    (1, "Terminado con errores"),
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


class Profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Perfiles'

    def __unicode__(self):
        return unicode(self.email)


class File(models.Model):
    fileUpload = models.FileField()
    description = models.TextField(default="")
    profile = models.ForeignKey(Profile)
    ext = models.CharField(max_length=7)

    class Meta:
        verbose_name_plural = 'Archivos'

    def __unicode__(self):
        return u"ARCHIVO \n Location: %s \n Description: %s " % (self.fileUpload.path, self.description)


class Proceso(models.Model):

    estado = models.IntegerField(choices=POSIBLES_ESTADOS_PROCESOS, default=3)
    std_err = models.TextField(default="")
    std_out = models.TextField(default="")
    comando = models.CharField(max_length=2000, default="echo Hola mundo")
    profile = models.ForeignKey(Profile)

    class Meta:
        verbose_name_plural = 'Procesos'

    def get_estado(self):
        return POSIBLES_ESTADOS_PROCESOS[self.estado][1]

    def run_process(self):
        self.estado = 2
        self.save()
        try:
            p = subprocess.Popen(str(self.comando), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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
        #  self.std_out = self.std_out.replace("\n", "<br>")
        #  self.std_err = self.std_err.replace("\n", "<br>")
        self.save()

    def run(self):
        t = threading.Thread(target=self.run_process)
        t.setDaemon(True)
        t.start()

    def __unicode__(self):
        return u"ID: %s Estado: %s \n Comando: %s \n STDOUT: \n %s \n STDERR: %s\n " % (str(self.id), str(self.estado), str(self.comando), str(self.std_out), str(self.std_err))


class Mapeo(models.Model):

    """"
    Ejemplo de mapeo
    type=1 -> Single end
    type=2 -> Paired end
    m = Mapeo(name="Exp", mapeador=0, tipo=1, profile=p)
    m.save()
    m.run_bowtie(reference="/home/null3d/Softs_ud/Abundace_Estimation-ud/files/ecoli.fa", reads_1=["/home/null3d/Softs_ud/Abundace_Estimation-ud/files/es_1_1_10k.fq"], reads_2=["/home/null3d/Softs_ud/Abundace_Estimation-ud/files/es_1_1_10k.fq"])
    """
    name = models.TextField(default="Experimento")
    procesos = models.ManyToManyField(Proceso)
    mapeador = models.IntegerField(choices=MAPEADORES, default=1)
    tipo = models.IntegerField(default=1, choices=TIPOS_MAPEO)
    profile = models.ForeignKey(Profile)
    out_file = models.ForeignKey(File, null=True)

    def run_bowtie(self, reference="", reads_1="", reads_2="", reads_se="", tipo=1):
        self.name = "Experimento %s" % self.id
        self.save()
        reference_file = reference  # Full path
        reference_path = reference_file[::-1].split("/", 1)[1][::-1]
        reference_index = reference_path + "/" + reference_file.split("/")[-1].replace(" ", "_").replace(".fasta", "").replace(".fa", "")
        comando = "bowtie-build %s %s" % (reference_file, reference_index)
        p1 = Proceso(comando=str(comando), profile=self.profile)
        p1.save()
        self.procesos.add(p1)
        # To get files with path trin.fileUpload.path
        # Genero indice y espero hasta que este listo
        t1 = threading.Thread(target=p1.run_process)
        t1.setDaemon(True)
        t1.start()
        while t1.isAlive():
            sleep(1)
        file_name = "/tmp/%s.bam" % self.name.replace(" ", "_")
        tmp_sam = "/tmp/%s" % ("tmp_%s.sam" % randint(1, 1000000))
        if self.tipo == 1:
            mates1 = ','.join(reads_1)
            mates2 = ','.join(reads_2)
            # out_bam = "%s.bam" % self.name.replace(" ", "_")samtools view -Sb - > hits.bam
            comando = "bowtie -a -S -p %s  %s -1 %s -2 %s %s  " % (settings.CORES, reference_index, mates1, mates2, tmp_sam)
        elif self.tipo == 0:
            mates = ",".join(reads_se)
            comando = "bowtie -a -S -p %s  %s -s %s  %s | samtools view -bSx - > %s " % (settings.CORES, reference_index, mates, tmp_sam)
        p2 = Proceso(comando=str(comando), profile=self.profile)
        p2.save()
        print p2
        self.procesos.add(p2)
        t2 = threading.Thread(target=p2.run_process)
        t2.setDaemon(True)
        t2.start()
        while t2.isAlive():
            sleep(1)
        comando = "samtools view -bS  %s -o %s" % (tmp_sam, file_name)
        p3 = Proceso(comando=str(comando), profile=self.profile)
        p3.save()
        self.procesos.add(p3)
        t3 = threading.Thread(target=p3.run_process)
        t3.setDaemon(True)
        t3.start()
        while t3.isAlive():
            sleep(1)
        self.save()
        out_file = File(fileUpload=Django_File(open(file_name)), description="Salida " + self.name, profile=self.profile, ext="bam")
        out_file.save()
        self.out_file = out_file

    def run(self, reference, reads_1="", reads_2="", reads_se="", tipo=1):
        t = threading.Thread(target=self.run_bowtie, kwargs=dict(reference=reference, reads_1=reads_1, reads_2=reads_2, reads_se=reads_se, tipo=tipo))
        t.setDaemon(True)
        t.start()

    class Meta:
        verbose_name_plural = "Procesos de mapeo"

    def __unicode__(self):
        return "MAPEO \n %s" % self.name


class Abundace_Estimation(models.Model):
    name = models.TextField(default="Abundace_Estimation Results")
    procesos = models.ManyToManyField(Proceso)
    out_results = models.ForeignKey(File, null=True, related_name="file_results_Abundace_Estimation")
    out_params = models.ForeignKey(File, null=True, related_name="file_rparams_Abundace_Estimation")
    profile = models.ForeignKey(Profile)

    def run_express(self, reference="", bam_file=""):
        self.name = "Abundace_Estimation Results. Exp: %s " % self.id
        self.save()
        out_dir = "/tmp/xprs_out%s" % str(randint(1, 65000))
        comando = "express -o %s %s %s" % (str(out_dir), reference, bam_file)
        p = Proceso(comando=str(comando), profile=self.profile)
        p.save()
        self.procesos.add(p)
        t1 = threading.Thread(target=p.run_process)
        t1.setDaemon(True)
        t1.start()
        while t1.isAlive():
            sleep(1)
        f1 = File(fileUpload=Django_File(open(out_dir + "/" + "results.xprs")), description="Salida " + self.name, profile=self.profile, ext="xprs")
        f1.save()
        self.out_results = f1
        f2 = File(fileUpload=Django_File(open(out_dir + "/" + "params.xprs")), description="Salida " + self.name, profile=self.profile, ext="xprs")
        f2.save()
        self.out_params = f2
        self.save()

    def run(self, reference="", bam_file=""):
        #  self.name = "Experimento %s" % self.id
        #  self.save()
        t = threading.Thread(target=self.run_express, kwargs=dict(reference=reference, bam_file=bam_file))  # Replace for bwa when ready
        t.setDaemon(True)
        t.run()

    def __unicode__(self):
        print name

    class Meta:
        verbose_name_plural = "Procesos de  estimar abundancia"  

