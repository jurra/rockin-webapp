from django.db import models

class Well(models.Model):
    id = models.AutoField(primary_key=True)
    well_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Well"
        verbose_name_plural = "Wells"
        app_label = "crudapp"