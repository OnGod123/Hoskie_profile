from django.db import models
from .person import Person  # Assuming Person model is defined in person.py

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
@classmethod
    def create_from_person(cls, person,profile_video=None):
        user_profile = cls(
            user=person,
            name=person.name,
            relationship_status=person.relationship_status,
            sexual_orientation=person.sexual_orientation,
            race=person.race,
            phone_number=person.phone_number,
            social_media_api=person.social_media_api,
            birth_date=person.birth_date,
            email=person.email,
            username=person.email
        )
        if profile_video:
            user_profile.profile_video = profile_video
        user_profile.save()
        return user_profile
