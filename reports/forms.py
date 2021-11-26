
from django import forms

from items.models import Item


class ReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    item = forms.ModelChoiceField(queryset=Item.objects.all().order_by("name"), required=False)
