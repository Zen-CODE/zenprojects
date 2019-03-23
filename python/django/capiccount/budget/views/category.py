"""
View classes for Categories
===========================
"""
from django.views.generic import ListView, DetailView
from budget.forms import CategoryForm
from budget.models import Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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
