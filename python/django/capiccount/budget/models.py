from django.db import models


class Account(models.Model):
    """
    A model of the account information
    """
    bank = models.TextField(max_length=50)
    type = models.TextField(max_length=50)
    account_number = models.IntegerField()
    name = models.TextField(max_length=50, default="Savings")


'''
Capitec's export to csv (not updated) provides the following columns:
     Account,Transaction Date,Journal Number,Transaction Type,Branch,
     Description,DebitAmount,CreditAmount,Narrative,BalanceAmount
     
e.g.
    1227278150,22/01/2019,17035382395,FINANCIAL,"",
    "Internet Banking Transfer to 1344338583 Stuart Bindon",850.00,,
    "STUART BINDON",23056.69
'''


class Category(models.Model):
    """
    Describes the type of transaction, so that we can separate transactions 
    into categories.
    """
    name = models.TextField(max_length=100)
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
    ''' The account based on the account number. '''

    transaction_date = models.DateField()

    journal_no = models.IntegerField()
    ''' The unique journal identifier, also specifying sequence. '''

    description = models.TextField()
    ''' A Textual description of the transaction. This is used to determine the
    category.'''

    credit = models.DecimalField(decimal_places=2, max_digits=100)
    ''' The amount credited to the account. This is negative if it's an expense.
    '''
    narrative = models.TextField()

    balance = models.DecimalField(decimal_places=2, max_digits=100)
    ''' The balance on the account after the amount has been credited. '''
