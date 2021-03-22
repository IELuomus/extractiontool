from django import forms
from .models import Pdf

class PageNumberForm(forms.Form):
    page_number  = forms.IntegerField()
    class Meta:
        fields = ['page_number']

class PdfForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ('title', 'author', 'pdf')
