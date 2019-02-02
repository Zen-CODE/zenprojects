from django import forms


class UploadCSVForm(forms.Form):
    """
    Handle the upload of the Capitec CSV file
    """
    title = forms.CharField(max_length=50)
    file = forms.FileField()
