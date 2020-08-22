from django import forms
from .models import Category, Categorization


class UploadCSVForm(forms.Form):
    """
    Handle the upload of the Capitec CSV file
    """
    file = forms.FileField()


class CategoryForm(forms.ModelForm):
    """
    Handles CRUD operation for the Category models.
    """

    class Meta:
        model = Category
        fields = ['name', 'importance']
        widgets = {
          'name': forms.Textarea(attrs={'rows': 1, 'cols': 50})}


class CategorizationForm(forms.ModelForm):
    """
    Handles CRUD operation for the Categorization models.
    """

    class Meta:
        model = Categorization
        fields = ['description', 'category']
        widgets = {
          'description': forms.Textarea(attrs={'rows': 1, 'cols': 50})}


class CategoryAnalysis(forms.Form):
    """
    Provide the data selection logic as parameters for category analysis
    """
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())
