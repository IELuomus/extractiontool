from django import forms

class PageNumberForm(forms.Form):
    page_number  = forms.IntegerField()
    class Meta:
        fields = ['page_number']