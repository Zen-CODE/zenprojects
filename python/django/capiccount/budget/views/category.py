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


class Analysis(object):
    """
    This class provides various functions around the analysis of costs by
    dividing the costs into Categories via Categorizations.
    """

    @staticmethod
    def get_analysis(trans_list):
        """
        Perform an analysis and return the results in the as a list, with each
        item in the list being a dictionary with the following keys:

            name: the name of the category
            total: the total amount spend in this category
            items: the number of items making up this total
        """

        def get_cat_count_dict(_cat, _cat_dict):
            """ Create and return a dictionary for the category used to track
            it's stats. Also add it to the _cat_dict with the name as it's key
            if it does not exist.
            """
            name = _cat.name if _cat is not None else "None"
            if name in _cat_dict.keys():
                return _cat_dict[name]
            else:
                _cat_dict[name] = {'items': 0, 'total': 0}
                return _cat_dict[name]

        cats = {}
        for trans in trans_list:
            cat = trans.get_category()
            cat_dict = get_cat_count_dict(cat, cats)
            cat_dict['items'] = cat_dict['items'] + 1
            cat_dict['total'] = cat_dict['total'] + trans.credit

        return cats

    @staticmethod
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
        # initial form ('cleaned_data'), so we can't access these values
        # generically in the template. We thus extract here and pass them in.
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

        trans_list = Transaction.objects.filter(
            transaction_date__lte=end_date, transaction_date__gte=start_date)
        return render(
            request,
            'budget/category_analysis.html',
            {'form': form,
             'trans_list': trans_list,
             'analysis': Analysis.get_analysis(trans_list),
             'start_date': start_date,
             'end_date': end_date})
