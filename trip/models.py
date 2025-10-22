from django.db import models
import json

class Trip(models.Model):
    current_location = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    cycle_used = models.IntegerField()
    total_miles = models.FloatField(null=True, blank=True)
    map_points_raw = models.TextField(null=True, blank=True)  # JSON string
    logs_raw = models.TextField(null=True, blank=True)        # JSON string
    created_at = models.DateTimeField(auto_now_add=True)

    def set_map_points(self, data):
        self.map_points_raw = json.dumps(data)

    def get_map_points(self):
        return json.loads(self.map_points_raw or "[]")

    def set_logs(self, data):
        self.logs_raw = json.dumps(data)

    def get_logs(self):
        return json.loads(self.logs_raw or "[]")

    def __str__(self):
        return f"Trip from {self.pickup_location} to {self.dropoff_location}"
