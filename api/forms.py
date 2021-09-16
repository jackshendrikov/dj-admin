from django import forms
from .utils.validators import validate_url, validate_country


class TestForm(forms.Form):
    link = forms.URLField(
        max_length=200,
        required=True,
        validators=[validate_url],
    )

    country = forms.CharField(
        max_length=128,
        required=True,
        validators=[validate_country],
    )

    source = forms.CharField(max_length=128, required=True)
    brand = forms.CharField(max_length=128, required=True)
    category = forms.CharField(required=True)
