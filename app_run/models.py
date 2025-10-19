from django.db import models
from django.contrib.auth.models import User


class Run(models.Model):
    STATUS_CHOICES = [
        ('init', 'Init'),
        ('in_progress', 'In progress'),
        ('finished', 'Finished'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='init',
    )

    def __str__(self):
        return f"Id {self.id} - Name {self.athlete} - Status {self.status}"


class AthleteInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goals = models.TextField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Id {self.id} - Name {self.user} - Goals {self.goals} - Weight {self.weight}"

