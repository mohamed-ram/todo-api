from django.db import models

CHOICES = (
    ('Hard', 'Hard'),
    ('Medium', 'Medium'),
    ('Easy', 'Easy'),
)

class Task(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=CHOICES)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return self.title


