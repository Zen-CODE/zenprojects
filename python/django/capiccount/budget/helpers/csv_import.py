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

    @staticmethod
    def _validate_csv(uploaded_file):
        """
        Return the (separator, col_names, lines) if it's a valid file, otherwise
        return False
        """
        try:
            f = uploaded_file.read().decode("utf-8")[1:-1]
        except UnicodeDecodeError:
            # Typical of a binary file
            return False

        f = f.split("\n")
        parts = f.pop(0).split("=")
        if len(parts) > 1:
            sep = parts[1]
            fields = f.pop(0).split(sep)
            if 'Journal Number' in fields:
                return sep, fields, f
        return False

    def load(self, uploaded_file):
        """
        Load the specified filename into the data, returning True if that
        works, False otherwise.

        The uploaded_file is a bytes object, starting and ending with a [ and ]
        respectively. See InMemoryUploadedFile
        """
        ret = self._validate_csv(uploaded_file)
        if ret:
            sep, fields, lines = ret
            recs = []
            while lines:
                parts = lines.pop(0).rstrip().split(sep)
                recs.append({fields[k]: parts[k] for k in range(len(fields))})

            self.records = recs
            return True
        else:
            return False

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
