from django import forms

from .models import category_choices


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    description = forms.CharField(widget=forms.Textarea)
    i_bid = forms.IntegerField(min_value=1)
    category = forms.ChoiceField(
        choices=category_choices,
    )
    custom_category = forms.CharField(max_length=20)
