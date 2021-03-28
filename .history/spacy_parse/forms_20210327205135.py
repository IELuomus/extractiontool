from django import forms
from .models import Pdf

class TraitValuesForm(forms.Form):
    traitvalues = forms.ar
    class Meta:
        fields = ['page_number']

