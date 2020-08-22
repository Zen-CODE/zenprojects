"""
# View classes for Transactions
# =============================
"""
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from budget.models import Transaction


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
