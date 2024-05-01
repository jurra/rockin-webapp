import json
import re

from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

DRILLING_MUD_CHOICES = [
        ('Water-based mud', 'Water-based mud'),
        ('Oil-based mud', 'Oil-based mud')
]

class Contact(models.Model):
    firstName = models.CharField(
        "First name", max_length=255, blank=True, null=True)
    lastName = models.CharField(
        "Last name", max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.firstName

# We need to create a custom field for the PositiveFloatField to set it always to positive
class PositiveFloatField(models.FloatField):
    def formfield(self, **kwargs):
        defaults = {'min_value': 0}
        defaults.update(kwargs)
        return super().formfield(**defaults)

class Well(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Well"
        verbose_name_plural = "Wells"
        app_label = "crudapp"

    def __str__(self):
        # This needs to be as is otherwise the form will display all fields of the model
        # in the dropdown menu
        return self.name
    
    def gen_short_name(self):
        short_name = re.split(r'[-\s]+', self.name)
        return ''.join(short_name)

class RockinBase(models.Model):
    well = models.ForeignKey(Well, on_delete=models.CASCADE,
                help_text="The id of the well", related_name='corechips_well')

    registration_date = models.DateTimeField(
        help_text="The time when the core was registered in the database",
        auto_now_add=True)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_date = models.DateTimeField(
        help_text="The date when the core was collected", default=timezone.now, null=True)
    remarks = models.CharField(
        max_length=255, help_text="The remarks of the section of a meter sample")

    drilling_mud = models.CharField(
        max_length=17,
        choices=DRILLING_MUD_CHOICES,
        null=True,
        blank=True,
        help_text="The drilling mud used for the perforation of the core"
    )
    lithology = models.CharField(
        max_length=255, null=True, blank=True, help_text="The lithology of the core")

    class Meta:
        abstract = True
    
    sample_weight = PositiveFloatField(
        null=True, blank=True, help_text="The weight of the sample in kilograms")


class CoreBase(RockinBase):
    CORE_SECTION_CHOICES = [
        ('C1', 'C1'),
        ('C2', 'C2'),
        ('C3', 'C3'),
        ('C4', 'C4'),
        ('C5', 'C5'),
        ('C6', 'C6'),
        ('C7', 'C7'),
        ('C8', 'C8'),
        ('C9', 'C9'),
    ]
    core_number = models.CharField(
        max_length=2, choices=CORE_SECTION_CHOICES,
        help_text="The predefined name of the core from C1 to C9")
    planned_core_number = models.CharField(
        max_length=2, choices=CORE_SECTION_CHOICES,
        help_text="The predefined name of the core from C1 to C9")

    core_section_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="The counter for all 1 meter sections of the core")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # If this is a new instance of the model, generate the core name based on the related well name
            well_name = self.well.name
            core_number = self.core_number
            core_section_number = Core.objects.filter(
                well=self.well).count() + 1
            self.core_section_name = f"{well_name}-{core_number}-{core_section_number}"
        super().save(*args, **kwargs)


class Core(CoreBase):
    # id = models.AutoField(primary_key=True, help_text="The id of the core")
    well = models.ForeignKey(Well, on_delete=models.CASCADE,
                             help_text="The name of the well", related_name='cores',
                             to_field='name')

    CORE_TYPE_CHOICES = [
        ('Core', 'Core'),
        ('Core catcher', 'Core catcher')
    ]
    core_section_name = models.CharField(
        max_length=255, 
        unique=True,
        help_text="The name of the section based on the well name, the core number and the core section number. See that CC has a sequential relationship with the core number and core section number")

    core_type = models.CharField(
        max_length=12,
        choices=CORE_TYPE_CHOICES,
        help_text="The type of the core",
        default=''
    )
    top_depth = PositiveFloatField(
        help_text="The top depth of the section of a meter sample")
    bottom_depth = PositiveFloatField(
        help_text="The bottom depth of the section of a meter sample", null=True, blank=True)
    core_section_length = PositiveFloatField(
        null=True,
        blank=True,
        help_text="The length of the section of a meter sample"
    )
    core_recovery = PositiveFloatField(
        null=True, blank=True, help_text="The recovery of the material in the core liner")
    core_diameter = PositiveFloatField(
        null=True, blank=True, help_text="The diameter of the core in inches")
    CORING_METHOD_CHOICES = [
        ('Motor', 'Motor'),
        ('Rotary', 'Rotary'),
        ('Both', 'Both')
    ]
    coring_method = models.CharField(
        max_length=6,
        choices=CORING_METHOD_CHOICES,
        null=True,
        blank=True,
        help_text="The method used for coring"
    )
    coreliner = models.CharField(
        max_length=255, null=True, blank=True, help_text="The material used for the core liner")
    formation = models.CharField(max_length=255, null=True, blank=True,
                                 help_text="The geological formation where the core was extracted from")
    CORE_STATUS_CHOICES = [
        ('Preserved', 'Preserved'),
        ('Opened', 'Opened')
    ]
    core_status = models.CharField(
        max_length=9,
        choices=CORE_STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="The status of the core"
    )
    PRESERVATION_CHOICES = [
        ('Refrigerated at 4 degrees Celsius', 'Refrigerated at 4 degrees Celsius'),
        ('Core rack at room temperature', 'Core rack at room temperature')
    ]
    preservation = models.CharField(
        max_length=35,
        choices=PRESERVATION_CHOICES,
        null=True,
        blank=True,
        help_text="The preservation method used for the core"
    )
    core_weight = PositiveFloatField(
        null=True, blank=True, help_text="The weight of the core in kilograms")
    ct_scanned = models.BooleanField(
        null=True, blank=True, help_text="Whether the core was CT scanned or not")
    macroct_scanned = models.BooleanField(
        null=True, blank=True, help_text="Whether the core was CT scanned or not")
    gamma_ray = models.BooleanField(
        null=True, blank=True, help_text="Whether the core was gamma ray scanned or not")
    radiation = PositiveFloatField(
        null=True, blank=True, help_text="The radiation of the core in Bq units")

    class Meta:
        db_table = 'core'
        verbose_name = "Core"
        verbose_name_plural = "Cores"

        indexes = [
            models.Index(fields=['core_number', 'core_section_number']),
        ]



    def __str__(self):
        serialized = model_to_dict(
            self, fields=[field.name for field in self._meta.fields])

        # Return a dictionary of all properties
        return json.dumps(serialized, indent=4, sort_keys=False)


class CoreChip(RockinBase):
    well = models.ForeignKey(Well, on_delete=models.CASCADE,
                             help_text="The name of the well", related_name='corechips',
                             to_field='name')
    core_section_name = models.CharField(
        max_length=255, 
        unique=False,
        help_text="The name of the section based on the well name, the core number and the core section number. See that CC has a sequential relationship with the core number and core section number")

    corechip_number = models.CharField(
        max_length=255, 
        unique=True,
        help_text="The predefined name of the core chip")
    FROM_TOP_BOTTOM_CHOICES = [
        ('Top', 'Top'),
        ('Bottom', 'Bottom')
    ]
    from_top_bottom = models.CharField(
        max_length=6,
        choices=FROM_TOP_BOTTOM_CHOICES,
        help_text="Whether the core chip was taken from the top or the bottom of the core"
    )
    corechip_name = models.CharField(
        max_length=255, 
        unique=True,
        help_text="The name of the core chip that is generated based on well_name, core_number, core_section_number, core_chip_number and from_top_bottom")
    corechip_depth = PositiveFloatField(
        help_text="The depth of the core chip in meters")

    formation = models.CharField(
        max_length=255, null=True, blank=True, help_text="The formation of the core chip")

    top_depth = PositiveFloatField(
        null=True,
        help_text="The top depth of the section of a meter sample")


class Cuttings(RockinBase):
    # id = models.AutoField(primary_key=True, help_text="The id of the core")
    well = models.ForeignKey(Well, on_delete=models.CASCADE,
                             help_text="The id of the well", related_name='cuttings_well',
                             to_field='name')
    cuttings_number = models.IntegerField(
        help_text="The predefined name of the cuttings")
    cuttings_name = models.CharField(
        max_length=255, 
        unique=True,
        help_text="The name of the cuttings")
    cuttings_depth = PositiveFloatField(
        help_text="The depth of the cuttings in meters")
    sample_state = models.CharField(max_length=100, choices=[('Wet washed', 'Wet washed'), (
        'Wet unwashed', 'Wet unwashed'), ('Dry washed', 'Dry washed')], help_text="The state of the sample")

    # Optional fields
    collection_method = models.CharField(max_length=8, null=True, blank=True, choices=[('Drilling', 'Drilling'), (
        'Coring', 'Coring'), ('Rathole', 'Rathole'), ('Flushing', 'Flushing')], help_text="The method used for collecting the cuttings")
    drilling_method = models.CharField(max_length=100, null=True, blank=True, choices=[(
        'Rotary', 'Rotary'), ('Motor', 'Motor'), ('Both', 'Both')], help_text="The method used for drilling")
    dried_sample = models.BooleanField(
        null=True, blank=True, help_text="Whether the sample was dried or not")
    dried_by = models.CharField(
        max_length=255, null=True, blank=True, help_text="The user who dried the sample")
    dried_date = models.DateTimeField(
        null=True, blank=True, help_text="The date when the sample was dried")

    class Meta:
        verbose_name = "Cuttings"
        verbose_name_plural = "Cuttings"


class MicroCore(models.Model):
    well = models.ForeignKey(Well, on_delete=models.CASCADE,
                help_text="The name of the well", related_name='corechips_well',
                to_field='name')

    registration_date = models.DateTimeField(
        help_text="The time when the core was registered in the database",
        auto_now_add=True)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_date = models.DateTimeField(
        help_text="The date when the core was collected", default=timezone.now)
    remarks = models.CharField(
        max_length=255, help_text="The remarks of the section of a meter sample")

    drilling_mud = models.CharField(
        max_length=17,
        choices=DRILLING_MUD_CHOICES,
        null=True,
        blank=True,
        help_text="The drilling mud used for the perforation of the core"
    )
    lithology = models.CharField(
        max_length=255, null=True, blank=True, help_text="The lithology of the core")

    micro_core_number = models.IntegerField(
        help_text="The predefined name of the micro core")
    micro_core_name = models.CharField(
        unique=True,
        max_length=255, help_text="The name of the micro core that is generated based on well_name")

    # Optional fields
    drilling_method = models.CharField(max_length=100, null=True, blank=True, choices=[(
        'Rotary', 'Rotary'), ('Motor', 'Motor'), ('Both', 'Both')], help_text="The method used for drilling")
    drilling_bit = models.CharField(
        max_length=255, null=True, blank=True, help_text="The bit used for drilling")

    class Meta:
        verbose_name = "Micro Core"
        verbose_name_plural = "Micro Cores"
