from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadCSVForm


def index(request):
    return HttpResponse("Hello, world. You're at the budget index.")


def import_csv(request):

    #return render(request, "import.html", {})
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadCSVForm()
    return render(request, 'import.html', {'form': form})
