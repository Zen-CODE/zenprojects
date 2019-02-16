from django.db import models


class Account(models.Model):
    """
    A model of the account information
    """
    bank = models.TextField(max_length=50)
    type = models.TextField(max_length=50)
    account_number = models.IntegerField()


'''
Capitec's export to csv (updated) provides the following columns:
     Sequence Number,Account,Posting Date,Transaction Date,
     Statement Description,Long Description,Parent Category,Sub-category,
     Debit Amount,Credit Amount,Balance
'''


class Category(models.Model):
    """
    Describes the type of transaction, so that we can separate transactions 
    into categories.
    """
    name = models.TextField()
    importance = models.IntegerField()


class Categorization(models.Model):
    """
    Describes how transactions are mapped to categories.
    """
    capi_category = models.TextField()
    capi_sub_category = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Transaction(models.Model):
    """
    Model of a transaction as described in the imported CSV file.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    posting_date = models.DateField()
    transaction_date = models.DateField()
    description = models.TextField()
    description_long = models.TextField()
    capi_category = models.TextField()
    capi_sub_category = models.TextField()
    credit = models.DecimalField(decimal_places=2, max_digits=100)
    ''' The amount credited to the account. This is negative if it's an expense.
    '''
    balance = models.DecimalField(decimal_places=2, max_digits=100)
    ''' The balance on the account after the amount has been credited. '''
