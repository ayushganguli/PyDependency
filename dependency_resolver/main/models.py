from django.db import models

class VirtualEnvironmentPath(models.Model):
    path_value = models.CharField(max_length=10000)
    def __str__(self) -> str:
        return self.path_value

# Create your models here.
