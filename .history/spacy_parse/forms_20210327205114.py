from django import forms
from .models import Pdf

class TraitValuesForm(forms.Form):
    traitvalues = forms.IntegerField()
    class Meta:
        fields = ['page_number']

