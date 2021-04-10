from django import forms
from django.contrib.postgres.forms import SimpleArrayField

class TraitValuesForm(forms.Form):
    traitvalues = forms.SimpleArrayField()
    class Meta:
        fields = ['page_number']

