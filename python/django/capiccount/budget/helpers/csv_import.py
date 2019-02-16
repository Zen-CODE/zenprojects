"""
A helper module to handle the import of Capitec CSV files
"""


class CapitecCSV(object):
    """
    Handles the unpacking of Capitec CSV files,
    """
    def __init__(self, file_name):
        super(CapitecCSV, self).__init__()

        with open(file_name, 'r') as f:
            # Read in the meta data included in the file
            sep = f.readline().rstrip().split("=")[1]
            fields = f.readline().rstrip().split(sep)

            recs = []
            for line in f.readlines():
                parts = line.rstrip().split(sep)
                recs.append({fields[k]: parts[k] for k in range(len(fields))})

        self.records = recs
        '''
        A list of dictionaries corresponding to each line in the csv file,
        ignoring the first two.
        '''

    def __str__(self):
        """ Override the string display method. """
        return str("\n".join([str(rec) for rec in self.records]))


def csv_import(csv_file):
    """
    Import the uploaded csv file
    """
    print("helpers.import: got file")
    for line in csv_file.readlines():
        print(">{0}".format(line.rstrip()))
