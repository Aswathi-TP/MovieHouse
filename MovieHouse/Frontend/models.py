from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Create your models here.
class RegistrationDB(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True)
    Password = models.CharField(max_length=100,null=True,blank=True)
    Email = models.EmailField(max_length=100, null=True, blank=True,unique=True)

class CustomUserManage(BaseUserManager):
    def _create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'),unique=True)
    username = models.CharField(_('username'),max_length=100,default='MovieHouse')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManage()


class ReviewDB(models.Model):
    user = models.CharField(max_length=100)
    movie = models.CharField(max_length=100)
    review = models.CharField(max_length=100,null=True,blank=True)
    rate = models.IntegerField(null=True,blank=True)
    date = models.DateField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_profile')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    place = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="profile",null=True,blank=True)


class TheatreSlotDB(models.Model):
    UserName = models.CharField(max_length=100,null=True,blank=True)
    TheatreName = models.CharField(max_length=100,null=True,blank=True)
    TheatreAddress = models.CharField(max_length=100, null=True, blank=True)
    MovieName = models.CharField(max_length=100, null=True, blank=True)
    SeatNum = models.CharField(max_length=100,null=True,blank=True)
    Date = models.CharField(max_length=100,null=True,blank=True)
    Time = models.CharField(max_length=100,null=True,blank=True)
    TotalPrice = models.CharField(max_length=100,null=True,blank=True)
    Created_at = models.DateTimeField()

class BookSlotDB(models.Model):
    UserName = models.CharField(max_length=100,null=True,blank=True)
    TheatreName = models.CharField(max_length=100,null=True,blank=True)
    TheatreAddress = models.CharField(max_length=100, null=True, blank=True)
    MovieName = models.CharField(max_length=100, null=True, blank=True)
    SeatNum = models.CharField(max_length=100,null=True,blank=True)
    Date = models.CharField(max_length=100,null=True,blank=True)
    Time = models.CharField(max_length=100,null=True,blank=True)
    TotalPrice = models.CharField(max_length=100,null=True,blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)

class ContactDB(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True)
    Email = models.EmailField(max_length=100,null=True,blank=True)
    Phone = models.CharField(max_length=100,null=True,blank=True)
    Message = models.CharField(max_length=500,null=True,blank=True)

class BookingDB(models.Model):
    book_id = models.CharField(max_length=100,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    movie_name = models.CharField(max_length=100,blank=True,null=True)
    theatre_name = models.CharField(max_length=100,blank=True,null=True)
    theatre_address = models.CharField(max_length=100,blank=True,null=True)
    selected_seats = models.CharField(max_length=100,blank=True,null=True)
    selected_date = models.CharField(max_length=100,blank=True,null=True)
    selected_time = models.CharField(max_length=100,blank=True,null=True)
    amount_paid = models.CharField(max_length=100,blank=True,null=True)
    paid_status = models.BooleanField(default=False)
    booked_date = models.DateTimeField(auto_now_add=True)