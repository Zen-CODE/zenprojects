"""
A helper module to handle the import of Capitec CSV files
"""


def csv_import(csv_file):
    """
    Import the uploaded csv file
    """
    print("helpers.import: got file")
    for line in csv_file.readlines():
        print(">{0}".format(line.rstrip()))
