from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadCSVForm, CategoryAnalysis
from .helpers.csv_import import csv_import
from django.forms import Form
from .models import Transaction, Category, Categorization
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CategoryForm, CategorizationForm
from django.core.paginator import Paginator
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

    return render(request, 'budget/category_analysis.html',
                  {'form': form,
                   'start_date': start_date, 'end_date': end_date})


# View classes for Categories
# ===========================


class CategoryList(ListView):
    model = Category
    form_class = CategoryForm


class CategoryDetail(DetailView):
    model = Category
    form_class = CategoryForm


class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm


class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm


class CategoryDelete(DeleteView):
    model = Category


# View classes for Categorizations
# ================================


class CategorizationList(ListView):
    model = Categorization
    form_class = CategorizationForm


class CategorizationDetail(DetailView):
    model = Categorization
    form_class = CategorizationForm


class CategorizationCreate(CreateView):
    model = Categorization
    form_class = CategorizationForm


class CategorizationUpdate(UpdateView):
    model = Categorization
    form_class = CategorizationForm


class CategorizationDelete(DeleteView):
    model = Categorization


# View classes for Transactions
# =============================

class TransactionList(ListView):
    model = Transaction

    def get(self, request, *args, **kwargs):
        """ Override the HTML GET request to provide pagination. """

        trans_list = Transaction.objects.order_by("-transaction_date")
        paginator = Paginator(trans_list, 20)  # Show 20 transactions per page

        if paginator.count > 0:
            page = request.GET.get('page')
            transactions = paginator.get_page(page)
        else:
            transactions = []
        return render(request, 'budget/transaction_list.html',
                      {'tran_list': transactions})


class TransactionDetail(DetailView):
    model = Transaction
