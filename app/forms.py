from django import forms
from app.models import *



class Contact(forms.ModelForm):
    class Meta:
        model = Help
        fields = ('name','phone','email','content')