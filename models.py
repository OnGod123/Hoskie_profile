from django.db import models
from .person import Person  # Assuming Person model is defined in person.py

class Location(models.Model):
    user = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"

class UserProfile(models.Model):
    user = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    profile_video = models.FileField(upload_to=user_video_upload_path, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Assuming Location model exists
    tweet = models.ImageField(upload_to='tweets/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    # Duplicated fields from Person
    name = models.CharField(max_length=60)
    relationship_status = models.CharField(max_length=15, choices=Person.RELATIONSHIP_CHOICES)
    sexual_orientation = models.CharField(max_length=10, choices=Person.SEXUAL_ORIENTATION_CHOICES)
    race = models.CharField(max_length=10, choices=Person.RACE_CHOICES)
    phone_number = models.CharField(max_length=15)
    social_media_api = models.URLField()
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    
    # New field
    username = models.CharField(max_length=30, unique=True)  # Adding username field

    def __str__(self):
        return self.username

