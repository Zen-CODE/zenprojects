from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadCSVForm
from .helpers.csv_import import csv_import
from django.forms import Form
from .models import Transaction, Category, Categorization
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CategoryForm, CategorizationForm


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
            success = 2 if csv_import(request.FILES['file']) else 1
            # url = reverse('budget:view_transactions',
            #               args=(success,))
            url = "view_transactions/" + str(success)
            return HttpResponseRedirect(url)
    else:
        form = UploadCSVForm()
    return render(request, 'import.html', {'form': form})


def view_transactions(request, imp=0):
    """ View the last transactions the were imported. """
    # trans = Transaction.objects.all()
    trans = Transaction.objects.order_by("-journal_no")
    number = len(trans)
    msg = ["", "Import failed...", "Import successful"][imp]
    return render(request, 'view_transactions.html', {'trans': trans[:20],
                                                      'msg': msg,
                                                      'number': number})


'''
View classes for Categories
===========================
'''


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


'''
View classes for Categorizations
================================
'''


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
