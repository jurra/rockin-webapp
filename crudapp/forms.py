from django import forms
from crudapp.models import Contact, Well, Core

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"