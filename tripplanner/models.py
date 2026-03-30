from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    days = models.IntegerField()
    budget = models.IntegerField()
    interests = models.TextField()
    itinerary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.destination