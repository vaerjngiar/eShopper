from django import forms


class ProductSizeApplyForm(forms.Form):
    size = forms.CharField(label='Size')
