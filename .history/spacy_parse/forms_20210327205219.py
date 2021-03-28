from django import forms
from django.contrib.postgres.forms import SimpleArrayField

class TraitValuesForm(forms.Form):
    traitvalues = forms.Sim
    class Meta:
        fields = ['page_number']

