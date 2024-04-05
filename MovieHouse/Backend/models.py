from django.db import models

# Create your models here.
class TheatreDB(models.Model):
    TheatreName = models.CharField(max_length=100,null=True,blank=True)
    TheatreAddress = models.CharField(max_length=100,null=True,blank=True)
    Contact = models.IntegerField(null=True,blank=True)
    Email = models.EmailField(max_length=100,null=True,blank=True)
    Screen = models.IntegerField(null=True,blank=True)
    Capacity = models.IntegerField(null=True,blank=True)
    Status = models.CharField(max_length=100,null=True,blank=True)
    TheatreImage = models.ImageField(upload_to="images",null=True,blank=True)

class ScreenDB(models.Model):
    Theatre = models.CharField(max_length=100,null=True,blank=True)
    ScreenName = models.CharField(max_length=100,null=True,blank=True)
    TotalSeat = models.IntegerField(null=True,blank=True)
    PremiumSeat = models.IntegerField(null=True,blank=True)
    StandardSeat = models.IntegerField(null=True,blank=True)

class MovieDB(models.Model):
    MovieName = models.CharField(max_length=100,null=True,blank=True)
    Synopsis = models.CharField(max_length=100,null=True,blank=True)
    Genre = models.CharField(max_length=100,null=True,blank=True)
    Language = models.CharField(max_length=100,null=True,blank=True)
    ReleaseDate = models.DateField(blank=True,null=True)
    Poster1 = models.ImageField(upload_to="Images",null=True,blank=True)
    Poster2 = models.ImageField(upload_to="Images",null=True,blank=True)
    Poster3 = models.ImageField(upload_to="Images",null=True,blank=True)
    Duration = models.CharField(max_length=100,null=True,blank=True)
    TrailerLink = models.URLField(max_length=200,blank=True,null=True)

class CastCrewDB(models.Model):
    Movie = models.CharField(max_length=100,null=True,blank=True)
    ActorName = models.CharField(max_length=100,null=True,blank=True)
    Character = models.CharField(max_length=100,null=True,blank=True)
    ActorImage = models.ImageField(upload_to="Images",null=True,blank=True)
    CrewName = models.CharField(max_length=100,null=True,blank=True)
    Role = models.CharField(max_length=100,null=True,blank=True)
    CrewImage = models.ImageField(upload_to="images",null=True,blank=True)

class ShowTimeDB(models.Model):
    Theatre = models.CharField(max_length=100,null=True,blank=True)
    Show = models.CharField(max_length=100,null=True,blank=True)
    Movie = models.CharField(max_length=100,null=True,blank=True)
    Time = models.DateTimeField()
    price = models.IntegerField()

class ShowDB(models.Model):
    Theatre = models.CharField(max_length=100,null=True,blank=True)
    Show1 = models.CharField(max_length=100,null=True,blank=True)
    Show2 = models.CharField(max_length=100, null=True, blank=True)
    Show3 = models.CharField(max_length=100, null=True, blank=True)
    Show4 = models.CharField(max_length=100, null=True, blank=True)
    Show5 = models.CharField(max_length=100, null=True, blank=True)
    Movie = models.CharField(max_length=100,null=True,blank=True)
    Time = models.DateTimeField()
    price = models.IntegerField()

class SeatDB(models.Model):
    Theatre_name = models.CharField(max_length=100,null=True,blank=True)
    Total_seat = models.IntegerField()
    Available = models.IntegerField()