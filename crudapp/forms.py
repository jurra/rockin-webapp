from django.forms import ModelForm, ModelChoiceField, TextInput, inlineformset_factory
from crudapp.models import Contact, Well, Core


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class WellForm(ModelForm):
    class Meta:
        model = Well
        fields = "__all__"

class CoreForm(ModelForm):
    class Meta:
        model = Core
        # Lest display for testing only the fields that are required
        labels = {
            'well': 'WellName',
            'core_number': 'CoreNumber',
            'core_section_number': 'CoreSectionNumber',
        }
        
        fields = "__all__"
        widgets = {
            'core_section_name': TextInput(attrs={'readonly': 'readonly'}),
        }

        def save(self, commit=True):
            instance = super().save(commit=False)
            well_name = instance.well.name
            core_number = instance.core_number
            core_section_number = Core.objects.filter(well=instance.well).count() + 1
            instance.core_section_name = f"{well_name}-{core_number}-{core_section_number}"
            if commit:
                instance.save()
            return instance

