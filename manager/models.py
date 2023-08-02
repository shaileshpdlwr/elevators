from django.db import models
from django.core.cache import cache
from .constants import DIRECTION_CHOICES,DOOR_CHOICES
# Create your models here.

class Elevator(models.Model):
    elevator_id = models.IntegerField(unique=True)
    current_floor = models.IntegerField(default=1)
    destination_floor = models.IntegerField(default=1)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='STOP')
    is_operational = models.BooleanField(default=True)
    door_status = models.CharField(max_length=10, choices=DOOR_CHOICES, default='CLOSED')
    def __str__(self):
        return f"Elevator {self.elevator_id}"
    
    def get_current_status(self):
        key = f"elevator:{self.elevator_id}:status"
        status = cache.get(key)
        if status is None:
            status = {
                "current_floor": self.current_floor,
                "destination_floor": self.destination_floor,
                "direction": self.direction,
                "is_operational": self.is_operational,
            }
            cache.set(key, status)
        return status
    
    def get_next_destination_floor(self):
        if self.direction == 'UP':
            next_floor = min(self.current_floor + 1, self.destination_floor)
        elif self.direction == 'DOWN':
            next_floor = max(self.current_floor - 1, self.destination_floor)
        else:
            next_floor = self.current_floor

        return next_floor

class Request(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor = models.IntegerField()
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"Request for Elevator {self.elevator} - Floor {self.floor}"
