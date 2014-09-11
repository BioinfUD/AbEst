from forms import *
from django.shortcuts import render
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
