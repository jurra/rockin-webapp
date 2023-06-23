from django.db import models
from django.utils import timezone

class Contact(models.Model):
    firstName = models.CharField("First name", max_length=255, blank = True, null = True)
    lastName = models.CharField("Last name", max_length=255, blank = True, null = True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank = True, null = True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.firstName

class Well(models.Model):
    id = models.AutoField(primary_key=True)
    well_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Well"
        verbose_name_plural = "Wells"
        app_label = "crudapp"

    def __str__(self):
        return self.well_name

class RockinBase(models.Model):
    registration_date = models.DateTimeField(help_text="The time when the core was registered in the database")
    well_name = models.CharField(max_length=255, help_text="The name of the well")
    registered_by = models.CharField(max_length=255, help_text="The user who registered the core")
    collection_date = models.DateTimeField(help_text="The date when the core was collected", default=timezone.now)
    remarks = models.CharField(max_length=255, help_text="The remarks of the section of a meter sample")
    DRILLING_MUD_CHOICES = [
        ('Water-based mud', 'Water-based mud'),
        ('Oil-based mud', 'Oil-based mud')
    ]
    drilling_mud = models.CharField(
        max_length=17,
        choices=DRILLING_MUD_CHOICES,
        null=True,
        blank=True,
        help_text="The drilling mud used for the perforation of the core"
    )
    lithology = models.CharField(max_length=255, null=True, blank=True, help_text="The lithology of the core")

    class Meta:
        abstract = True

class CoreBase(RockinBase):
    core_number = models.CharField(max_length=2, help_text="The predefined name of the core from C1 to C9")
    planned_core_number = models.CharField(max_length=2, help_text="The predefined name of the core from C1 to C9")

    #FIXME: core_section_number = models.IntegerField(help_text="The counter for all 1 meter sections of the core")
    core_section_number = models.AutoField(unique=True, help_text="The counter for all 1 meter sections of the core")
    core_section_name = models.CharField(max_length=255, help_text="The name of the section based on the well name, the core number and the core section number. See that CC has a sequential relationship with the core number and core section number")

    class Meta:
        abstract = True

class Core(CoreBase):
    id = models.AutoField(primary_key=True, help_text="The id of the core")
    well= models.ForeignKey(Well, on_delete=models.CASCADE, help_text="The id of the well", related_name='cores_well')

    CORE_TYPE_CHOICES = [
        ('Core', 'Core'),
        ('Core catcher', 'Core catcher')
    ]
    core_type = models.CharField(
        max_length=12,
        choices=CORE_TYPE_CHOICES,
        help_text="The type of the core",
        default=''
    )
    top_depth = models.FloatField(help_text="The top depth of the section of a meter sample")
    bottom_depth = models.FloatField(help_text="The bottom depth of the section of a meter sample", null=True, blank=True)
    core_section_length = models.FloatField(
        null=True,
        blank=True,
        help_text="The length of the section of a meter sample"
    )
    core_recovery = models.FloatField(null=True, blank=True, help_text="The recovery of the material in the core liner")
    core_diameter = models.FloatField(null=True, blank=True, help_text="The diameter of the core in inches")
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
    coreliner = models.CharField(max_length=255, null=True, blank=True, help_text="The material used for the core liner")
    formation = models.CharField(max_length=255, null=True, blank=True, help_text="The geological formation where the core was extracted from")
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
    core_weight = models.FloatField(null=True, blank=True, help_text="The weight of the core in kilograms")
    ct_scanned = models.BooleanField(null=True, blank=True, help_text="Whether the core was CT scanned or not")
    gamma_ray = models.BooleanField(null=True, blank=True, help_text="Whether the core was gamma ray scanned or not")
    radiation = models.FloatField(null=True, blank=True, help_text="The radiation of the core in Bq units")

    class Meta:
        db_table = 'core'    

class CoreChip(RockinBase):
    id = models.AutoField(primary_key=True, help_text="The id of the core")
    well= models.ForeignKey(Well, on_delete=models.CASCADE, help_text="The id of the well", related_name='corechips_well')
    core_id = models.ForeignKey(
        'Core',
        on_delete=models.CASCADE,
        help_text="The id of the core",
        related_name='core_chips'
    )
    core_chip_number = models.IntegerField(help_text="The predefined name of the core chip")
    FROM_TOP_BOTTOM_CHOICES = [
        ('Top', 'Top'),
        ('Bottom', 'Bottom')
    ]
    from_top_bottom = models.CharField(
        max_length=6,
        choices=FROM_TOP_BOTTOM_CHOICES,
        help_text="Whether the core chip was taken from the top or the bottom of the core"
    )
    core_chip_name = models.CharField(max_length=255, help_text="The name of the core chip that is generated based on well_name, core_number, core_section_number, core_chip_number and from_top_bottom")
    core_chip_depth = models.FloatField(help_text="The depth of the core chip in meters")
    lithology = models.CharField(max_length=255, help_text="The lithology of the core chip")
    remarks = models.CharField(max_length=255, help_text="The remarks of the core chip")
    debris = models.BooleanField(null=True, blank=True, help_text="Whether the core chip is a debris or not")
    formation = models.CharField(max_length=255, null=True, blank=True, help_text="The formation of the core chip")

class Cuttings(RockinBase):
    id = models.AutoField(primary_key=True, help_text="The id of the core")
    well= models.ForeignKey(Well, on_delete=models.CASCADE, help_text="The id of the well", related_name='cuttings_well')
    cuttings_number = models.IntegerField(help_text="The predefined name of the cuttings")
    cuttings_name = models.CharField(max_length=255, help_text="The name of the cuttings")
    cuttings_depth = models.FloatField(help_text="The depth of the cuttings in meters")
    sample_state = models.CharField(max_length=100, choices=[('Wet washed', 'Wet washed'), ('Wet unwashed', 'Wet unwashed'), ('Dry washed', 'Dry washed')], help_text="The state of the sample")

    # Optional fields
    collection_method = models.CharField(max_length=8, null=True, blank=True, choices=[('Drilling', 'Drilling'), ('Coring', 'Coring'), ('Rathole', 'Rathole'), ('Flushing', 'Flushing')], help_text="The method used for collecting the cuttings")
    drilling_method = models.CharField(max_length=100, null=True, blank=True, choices=[('Rotary', 'Rotary'), ('Motor', 'Motor'), ('Both', 'Both')], help_text="The method used for drilling")
    sample_weight = models.FloatField(null=True, blank=True, help_text="The weight of the sample in kilograms")
    dried_sample = models.BooleanField(null=True, blank=True, help_text="Whether the sample was dried or not")
    dried_by = models.CharField(max_length=255, null=True, blank=True, help_text="The user who dried the sample")
    dried_date = models.DateTimeField(null=True, blank=True, help_text="The date when the sample was dried")

    class Meta:
        verbose_name = "Cuttings"
        verbose_name_plural = "Cuttings"

class MicroCore(RockinBase):
    id = models.AutoField(primary_key=True, help_text="The id of the core")
    well= models.ForeignKey(Well, on_delete=models.CASCADE, help_text="The id of the well", related_name='microcores_well')
    micro_core_number = models.IntegerField(help_text="The predefined name of the micro core")
    micro_core_name = models.CharField(max_length=255, help_text="The name of the micro core that is generated based on well_name")

    # Optional fields
    drilling_method = models.CharField(max_length=100, null=True, blank=True, choices=[('Rotary', 'Rotary'), ('Motor', 'Motor'), ('Both', 'Both')], help_text="The method used for drilling")
    drilling_bit = models.CharField(max_length=255, null=True, blank=True, help_text="The bit used for drilling")

    class Meta:
        verbose_name = "Micro Core"
        verbose_name_plural = "Micro Cores"

