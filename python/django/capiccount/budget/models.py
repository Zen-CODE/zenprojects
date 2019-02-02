from django.db import models


class Account(models.Model):
    """
    A model of the account information
    """
    bank = models.TextField(max_length=200)
    type = models.TextField(max_length=200)
    number = models.IntegerField()
    models.DecimalField(decimal_places=2, max_digits=100)


class Transaction(models.Model):
    """
    Model of a transaction as described in the imported CSV file.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    sequence_no = models.IntegerField()
    posting_date = models.DateField()
    transaction_date = models.DateField()
    description = models.TextField(max_length=200)
    credit = models.DecimalField(decimal_places=2, max_digits=100)
    balance = models.DecimalField(decimal_places=2, max_digits=100)
