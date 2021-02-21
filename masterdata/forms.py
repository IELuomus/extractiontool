from django import forms


class SourceDataImportForm(forms.Form):
    source_name = forms.CharField(max_length=255)
    file = forms.FileField(label="Upload a CSV file containing source data")
