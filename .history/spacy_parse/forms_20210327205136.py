from django import forms
from .models import Pdf

class TraitValuesForm(forms.Form):
    traitvalues = forms.arr
    class Meta:
        fields = ['page_number']

