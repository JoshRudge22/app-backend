from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db.models.signals import post_save

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Transgender', 'Transgender'),
    ('Prefer not to say', 'Prefer not to say')
]

def age(value):
    if value < 18:
        raise ValidationError('Must be 18 or over.')

def phone(number):
    if len(number) != 11 or not number.isdigit():
        raise ValidationError('Number must be 11 digits.')

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    age = models.IntegerField(validators=[age])
    phone_number = models.CharField(max_length=11, validators=[phone])
    email = models.EmailField(validators=[EmailValidator(message='Please enter a valid email address.')])
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default='Prefer not to say',
        blank=False 
    )
    profile_image = models.ImageField(upload_to='images/', default='images/default_profile_tpcl4s')

    def __str__(self):
        return f'{self.first_name} ({self.age}, {self.gender})'

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)

post_save.connect(create_profile, sender=User)