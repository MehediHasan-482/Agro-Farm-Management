from django.db import models
from accounts.models import Animal

# Create your models here.

class Disease(models.Model):
    animal_tag = models.ForeignKey(Animal,on_delete=models.CASCADE,related_name='diseases')
    disease_description = models.TextField()
    already_given_vaccine_name = models.CharField(max_length=50)
    vaccine_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.animal_tag} - {self.disease_description}"
