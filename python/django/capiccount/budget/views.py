from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadCSVForm
from .helpers.csv_import import csv_import
from django.forms import Form
from .models import Transaction


def index(_request):
    """ The landing page. """
    return HttpResponse("Hello, world. You're at the budget index.")


def delete(request):
    """ Delete all records. """
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            if 'delete' in request.POST:
                print("Delete all records!")
            else:
                print("Cancelled!")
            return HttpResponseRedirect('/budget/view_transactions')
    else:
        form = Form
    return render(request, 'delete.html', {'form': form})


def import_csv(request):
    """ Import transaction from the Capitec csv file export."""
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_import(request.FILES['file'])
            return HttpResponseRedirect('/budget/view_transactions')
    else:
        form = UploadCSVForm()
    return render(request, 'import.html', {'form': form})


def view_transactions(request):
    """ View the last transactions the were imported. """
    trans = Transaction.objects.all()
    print("No. of transaction = ", len(trans))
    return render(request, 'view_transactions.html', {'trans': trans})
