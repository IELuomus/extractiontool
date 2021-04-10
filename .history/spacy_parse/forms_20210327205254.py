from django import forms
from django.contrib.postgres.forms import SimpleArrayField

class TraitValuesForm(forms.Form):
    traitvalues = SimpleArrayField(forms.CharField(max_length=100))
    class Meta:
        fields = ['traitvalues']

