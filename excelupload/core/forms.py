from django import forms

class SalesForm(forms.Form):
    excel_file = forms.FileField()