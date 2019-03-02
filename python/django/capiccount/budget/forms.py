from django.forms import Form, ModelForm, FileField, Textarea
from .models import Category


class UploadCSVForm(Form):
    """
    Handle the upload of the Capitec CSV file
    """
    file = FileField()


class CategoryForm(ModelForm):
    """
    Handles CRUD operation for the Category models.
    """

    class Meta:
        model = Category
        fields = ['name', 'importance']
        widgets = {
          'name': Textarea(attrs={'rows': 1, 'cols': 50})}
