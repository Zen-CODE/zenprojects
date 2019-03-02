from django.forms import Form, ModelForm, FileField, Textarea
from .models import Category, Categorization


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


class CategorizationForm(ModelForm):
    """
    Handles CRUD operation for the Categorization models.
    """

    class Meta:
        model = Categorization
        fields = ['description', 'category']
        widgets = {
          'description': Textarea(attrs={'rows': 1, 'cols': 50})}
