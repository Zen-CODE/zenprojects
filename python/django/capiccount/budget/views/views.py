from django.shortcuts import render
from django.http import HttpResponseRedirect
from budget.forms import UploadCSVForm
from budget.helpers.csv_import import csv_import
from django.forms import Form
from budget.models import Transaction
from django.urls import reverse


def index(request):
    """ The landing page. """
    return render(request, 'index.html', {})


def clear(request):
    """ Delete all records. """

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            if 'delete' in request.POST:
                Transaction.objects.all().delete()
            return HttpResponseRedirect(reverse("budget:transaction_list"))
    else:
        form = Form
    return render(request, 'delete.html', {'form': form})


def import_csv(request):
    """ Import transaction from the Capitec csv file export."""
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            success = 1 if csv_import(request.FILES['file']) else 0
            # url = reverse('budget:view_transactions',
            #               args=(success,))
            url = "import_result/" + str(success)
            return HttpResponseRedirect(url)
    else:
        form = UploadCSVForm()
    return render(request, 'import.html', {'form': form})


def import_result(request, success):
    """ Display the results of the csv import. """

    return render(request, 'import_result.html', {'success': success})



