import uuid
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
    slots = models.CharField(
        max_length=500,
        help_text="Comma-seperated time slots (e.g. '6PM to 7PM, 7PM to 8PM, 8PM to 9PM' or 'Morning, Evening')"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_slots_list(self):
        slots = [s.strip() for s in self.slots.split(",") if s.strip()]
        return slots

    def __str__(self):
        return f"{self.name} ({self.date})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'description': self.description,
            'slots': self.get_slots_list(),
            'is_active': self.is_active,
            'created_at': self.created_at
        }

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')

    phone_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    slot = models.CharField(max_length=25) # selected slot from Event.slots

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_checked_in = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.event.name}"
    
    def to_dict(self):
        return {
            'event': self.event.to_dict(),
            'slot': self.slot,
            'full_name': self.full_name,
            'is_checked_in': self.is_checked_in,
            'token': self.token,
            'created_at': self.created_at
        }

