from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadCSVForm


def index(_request):
    """ The landing page. """
    return HttpResponse("Hello, world. You're at the budget index.")


def import_csv(request):

    # return render(request, "import.html", {})
    print("# Request.method: {0}".format(request.method))
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            print("# Handle uploaded file!")
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/budget/view_transactions')
    else:
        form = UploadCSVForm()
    return render(request, 'import.html', {'form': form})


def view_transactions(request):
    """ View the last transactions the were imported. """
    return render(request, 'view_transactions.html', {})
