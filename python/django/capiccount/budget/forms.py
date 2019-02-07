from django import forms


class UploadCSVForm(forms.Form):
    """
    Handle the upload of the Capitec CSV file
    """
    file = forms.FileField()
