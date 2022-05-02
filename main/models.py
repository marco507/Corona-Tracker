from django.db import models

class Record(models.Model):
    country = models.CharField(max_length=100)
    total_infections = models.IntegerField()
    total_deaths = models.IntegerField()
    incidence = models.DecimalField(max_digits=7, decimal_places=1)
    date = models.DateField(auto_now_add=True)
