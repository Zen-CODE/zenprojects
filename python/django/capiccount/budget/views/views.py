from django.shortcuts import render
from django.http import HttpResponseRedirect
from budget.forms import UploadCSVForm, CategoryAnalysis
from budget.helpers.csv_import import csv_import
from django.forms import Form
from budget.models import Transaction
from datetime import datetime
from calendar import monthrange


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
            return HttpResponseRedirect('/budget/view_transactions')
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


def category_analysis(request):
    """
    Show a category analysis between the dates specified.
    """
    def get_def_dates():
        """ Return the start and end dates of the current month """
        today = datetime.today()
        _start_date = today.replace(day=1)
        last_day = monthrange(today.year, today.month)[1]
        _end_date = today.replace(day=last_day)
        return _start_date, _end_date

    # The processed form has the date values in a different place to the
    # initial form ('cleaned_data'), so we can't access these values generically
    # in the template. We thus extract here and pass them in.
    if request.method == 'POST':
        form = CategoryAnalysis(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
        else:
            start_date, end_date = get_def_dates()
    else:
        start_date, end_date = get_def_dates()
        form = CategoryAnalysis(initial={'start_date': start_date,
                                         'end_date': end_date})

    trans_list = Transaction.objects.filter(transaction_date__lte=end_date,
                                            transaction_date__gte=start_date)
    return render(request, 'budget/category_analysis.html',
                  {'form': form, 'trans_list': trans_list,
                   'start_date': start_date, 'end_date': end_date})


