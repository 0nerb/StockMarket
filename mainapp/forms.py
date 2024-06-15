
from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email address', max_length=254)
