from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Barangay(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

class DisasterAlert(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_issued = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    alert_level = models.CharField(max_length=50, choices=[
        ('Info', 'Information'),
        ('Warning', 'Warning'),
        ('Severe', 'Severe'),
    ])

    def __str__(self):
        return f"{self.title} ({self.alert_level})"

class IncidentReport(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, related_name='incidents')
    location = models.CharField(max_length=255)
    description = models.TextField()
    incident_type = models.CharField(max_length=100)
    date_reported = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    image = models.ImageField(upload_to='incident_images/', blank=True, null=True)

    def __str__(self):
        return f"Incident at {self.location} - {self.status}"

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, related_name='shelters')
    capacity = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    @property
    def is_full(self):
        return self.current_occupancy >= self.capacity

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_profile')
    contact_number = models.CharField(max_length=15)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, related_name='volunteers')
    date_joined = models.DateField(default=timezone.now)
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.barangay})"

class ReliefDistribution(models.Model):
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, related_name='relief_distributions')
    date = models.DateTimeField()
    items = models.TextField()
    distribution_point = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Relief Distribution - {self.barangay.name} on {self.date}"

class EmergencyResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('Guide', 'Guide'),
        ('Checklist', 'Checklist'),
        ('Contact', 'Emergency Contact'),
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES)
    content = models.TextField()
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.resource_type})"

class Donation(models.Model):
    donor_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    donation_type = models.CharField(max_length=100)
    description = models.TextField()
    date_donated = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation by {self.donor_name} - {self.donation_type}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class DisasterStatistics(models.Model):
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, related_name='statistics')
    disaster_type = models.CharField(max_length=100)
    occurrences = models.IntegerField(default=0)
    casualties = models.IntegerField(default=0)
    damages = models.DecimalField(max_digits=12, decimal_places=2)  # Total cost of damages
    date_recorded = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.disaster_type} in {self.barangay} - {self.date_recorded}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    date_sent = models.DateTimeField(default=timezone.now)
    response = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback from {self.name or 'Anonymous'} on {self.date_sent}"
