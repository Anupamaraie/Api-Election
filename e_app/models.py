from django.db import models

# Create your models here.
class Main(models.Model):
    updated_time = models.TimeField()
    
    
class Election_Area(models.Model):
    election_area=models.CharField(max_length=100)
    time = models.ForeignKey(Main,on_delete=models.CASCADE,related_name='data')
    
    def __str__(self):
        return self.election_area
    
class Details(models.Model):
    name=models.CharField(max_length=100)
    party=models.CharField(max_length=100)
    vote=models.IntegerField()
    area = models.ForeignKey(Election_Area,on_delete=models.CASCADE,related_name='candidates',null=True,blank=True)
    
    def __str__(self):
        return self.name
    