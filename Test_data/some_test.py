 rm db.sqlite3 && python2 manage.py migrate && python2 manage.py shell



from django.contrib.auth.models import User
from processing.models import *

email="trin@yopmail.com"
user = "trin"
password="lol"
u = User(username=email,email=email)
u.set_password(password)
u.save()
p = Profile(user=u,
               email=email,
                firstName="N",
               lastName="N")
p.save()

p = Profile.objects.get(id=1)
m = Mapeo(name="Experimento", mapeador=0, tipo=1, profile=p)
m.save()
m.run(reference="/home/null3d/Git_repos/expdiff-ud/files/ecoli.fa", reads_1=["/home/null3d/Git_repos/expdiff-ud/files/s_1_1_10k.fq"], reads_2=["/home/null3d/Git_repos/expdiff-ud/files/s_1_2_10k.fq"], tipo=1)

from processing.models import *
p = Profile.objects.get(id=1)
ab = Abundace_Estimation(profile=p)
ab.run(reference="/home/null3d/Git_repos/expdiff-ud/files/ecoli.fa", bam_file="/home/null3d/Git_repos/expdiff-ud/files/Experimento_1_OMlyWGW.bam", )

mapeo = Mapeo(name="Exp", mapeador=0, tipo=1, profile=new_profile)
mapeo.save()
mapeo.run_bowtie(reference="popo")

	
express -o /tmp/lol /home/null3d/Softs_ud/expdiff-ud/files/ecoli.fa /home/null3d/Git_repos/expdiff-ud/files/Exp.bam


s_1_1_10k.fq  s_1_2_10k.fq
 bowtie -S -p 8 -1 /home/null3d/Git_repos/expdiff-ud/files/s_1_1_10k.fq -2 /home/null3d/Git_repos/expdiff-ud/files/s_1_2_10k.fq