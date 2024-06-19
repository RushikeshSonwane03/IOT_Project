from django.db import models

# Create your models here.

class Rider(models.Model):
    RiderName = models.CharField(max_length=200)
    RiderMail = models.CharField(max_length=50)
    RiderHeight = models.FloatField()
    RiderWeight = models.FloatField()
    RiderBMI = models.FloatField()
    RiderMass = models.FloatField()
    
    def __str__(self):
        return self.RiderName    


class Features(models.Model):
    RiderName = models.CharField(max_length=200)
    RiderBMI = models.FloatField()
    RiderMass = models.FloatField()
    RiderAcceleration = models.FloatField()
    RiderAppliedForce = models.FloatField()
    
    def __str__(self):
        return self.RiderName
    
class Prediction_Output(models.Model):
    RiderName = models.CharField(max_length=200)
    RiderAppliedForce = models.FloatField()
    RiderPredictedForce = models.FloatField()
    ForceDifference = models.FloatField()
    
    def __str__(self):
        return self.RiderName