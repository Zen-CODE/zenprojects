"""
A helper module to handle the import of Capitec CSV files
"""
from budget.models import Transaction, Account
from datetime import date


class CapitecCSV(object):
    """
    Handles the unpacking of Capitec CSV files,
    """
    def __init__(self):
        super(CapitecCSV, self).__init__()
        self.records = []
        '''
        A list of dictionaries corresponding to each line in the csv file,
        ignoring the first two.
        '''

    def load(self, file_name):
        """ Load the specified filename into the data, returning True if that
        works, False otherwise. """
        # The file _name ia bytes object, starting and ending with a [ and ]
        # respectively
        f = file_name.read().decode("utf-8")[1:-1]
        f = f.split("\n")
        sep = f.pop(0).split("=")[1]
        fields = f.pop(0).split(sep)

        recs = []
        while f:
            line = f.pop(0)
            parts = line.rstrip().split(sep)
            recs.append({fields[k]: parts[k] for k in range(len(fields))})

        self.records = recs
        return True
#        except Exception as e:
#            return False
#
    def __str__(self):
        """ Override the string display method. """
        return str("\n".join([str(rec) for rec in self.records]))

    def do_import(self):
        """
        Import the load csv file
        """
        objects = Transaction.objects
        for line in self.records:

            # Ensure the journal entry does not already exist
            query_set = objects.filter(journal_no=int(line['Journal Number']))
            if len(query_set) == 0:

                # Setup the data
                credit = float(line['CreditAmount']) if line['CreditAmount'] \
                    else -float(line['DebitAmount'])
                date_parts = [int(p) for p in reversed(
                    line['Transaction Date'].split('/'))]
                acc = Account.objects.get(account_number=int(line['Account']))

                Transaction(
                    account=acc,
                    transaction_date=date(*date_parts),
                    journal_no=int(line['Journal Number']),
                    description=line['Description'],
                    credit=credit,
                    narrative=line['Narrative'],
                    balance=float(line['BalanceAmount'])).save()


def csv_import(csv_file):
    """
    Import the uploaded csv file
    """
    csv = CapitecCSV()
    if csv.load(csv_file):
        print("Loaded. About to do import")
        csv.do_import()
        return True
    return False

    # for line in csv_file.readlines():
    #     print(">{0}".format(line.rstrip()))
