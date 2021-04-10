from django import forms
from .models import Pdf

class TraitValuesForm(forms.Form):
    page_number  = forms.IntegerField()
    class Meta:
        fields = ['page_number']

