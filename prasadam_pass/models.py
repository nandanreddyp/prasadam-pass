import uuid
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.date})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at
        }

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')

    phone_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_checked_in = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.event.name}"
    
    def to_dict(self):
        return {
            'event': self.event.to_dict(),
            'full_name': self.full_name,
            'is_checked_in': self.is_checked_in
        }

