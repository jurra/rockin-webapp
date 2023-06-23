from django.forms import ModelForm, inlineformset_factory
from crudapp.models import Contact, Well, Core


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class WellForm(ModelForm):
    class Meta:
        model = Well
        fields = "__all__"


# CoreFormSet = inlineformset_factory(
#     Well, Core, fields=['depth_from', 'depth_to'], extra=1)
