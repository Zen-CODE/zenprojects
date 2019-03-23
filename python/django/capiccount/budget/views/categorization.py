"""
View classes for Categorizations
================================
"""
from django.views.generic import ListView, DetailView
from budget.forms import CategorizationForm
from budget.models import Transaction, Categorization
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


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
    form_class = CategorizationForm


def cat_assign(request, pk):
    """
    Assign or update the categorization for the specified transaction. As this
    categorization is based on a real-time lookup, we need to do a lookup to
    find the applicable transaction (if there is one).
    """
    def save_categorization(_categorization, descrip, category):
        """ Update and save to supplied categorization"""
        _categorization.description = descrip
        _categorization.category = category
        _categorization.save()

    trans = Transaction.objects.get(pk=pk)
    categorization = Categorization.objects.all().filter(
        description=trans.description)
    if request.method == 'POST':
        form = CategorizationForm(request.POST)
        if form.is_valid():
            if categorization:
                save_categorization(categorization[0],
                                    form.cleaned_data['description'],
                                    form.cleaned_data['category'])
            else:
                form.save()
            return HttpResponseRedirect(reverse("budget:transaction_detail",
                                                args=[pk]))
    elif categorization:  # Update existing
        form = CategorizationForm(instance=categorization[0])
    else:  # Create
        form = CategorizationForm(
            initial={'description': trans.description})
    return render(request, 'budget/categorization_form.html', {'form': form})
