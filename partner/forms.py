from django import forms


class PartnerForm(forms.Form):
    excel_sheet = forms.FileField()
    logo = forms.ImageField()
