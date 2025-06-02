from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('ON_HOLD', 'On Hold'),
        ('CURRENT', 'Current'),
        ('UPCOMING', 'Upcoming'),
        ('COMPLETED', 'Completed')
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='UPCOMING'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )
    order = models.IntegerField(default=0)  # For drag and drop ordering
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['status', 'order', '-created_at'] 