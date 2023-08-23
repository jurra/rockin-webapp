from django.forms import ModelForm, ModelChoiceField, TextInput, inlineformset_factory
from crudapp.models import Contact, Well, Core, CoreChip, MicroCore


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
            'well': 'Well Name',
            'core_number': 'Core Number',
            'core_section_number': 'Core Section Number',
        }
        
        fields = "__all__"
        exclude = [
                   'registered_by',

                   # THIS EXCLUSION IS JUST FOR DEV PURPOSES
                   'formation',
                   'lithology',
                   'core_weight',
                   'core_length',
                   'gamma_ray',
                   'radiation',
                   'ct_scanned',
                   'bottom_depth'
                   ]
        
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

class CoreChipForm(ModelForm):
    class Meta:
        model = CoreChip

        labels = {
            'well': 'Well Name',
            'core_number': 'Core Number',
            'core_section_number': 'Core Section Number',
        }

        fields = "__all__"

        exclude = [
            'registered_by',
        ]

        widgets = {
            'core_section_name': TextInput(attrs={'readonly': 'readonly'}),
        }

class MicroCoreForm(ModelForm):
    class Meta:
        model = MicroCore
        fields = "__all__"

        