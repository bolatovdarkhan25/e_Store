from django import forms
from django.utils import timezone
from . import models


class OrderForm(forms.Form):
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Самовывоз"), ("delivery", "Доставка")]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField()
    comments = forms.CharField(widget=forms.Textarea, required=False)
