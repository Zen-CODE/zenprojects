"""
View classes for Categories
===========================
"""
from django.views.generic import ListView, DetailView
from budget.forms import CategoryForm
from budget.models import Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datetime import datetime
from calendar import monthrange
from budget.forms import CategoryAnalysis
from django.shortcuts import render
from budget.models import Transaction


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


def analysis(request):
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
                  {'form': form, 'trans_list': trans_list, 'cat_summary': [],
                   'start_date': start_date, 'end_date': end_date})
