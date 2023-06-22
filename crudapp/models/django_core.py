from django.db import models
from crudapp.models.django_well import Well

class Core(models.Model):
    id = models.AutoField(primary_key=True)
    well = models.ForeignKey(Well, on_delete=models.CASCADE, related_name='cores')
    # other fields ...

    class Meta:
        verbose_name = "Core"
        verbose_name_plural = "Cores"
        app_label = "src.crudapp"