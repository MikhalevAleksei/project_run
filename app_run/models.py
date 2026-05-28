from django.db import models
from django.contrib.auth.models import User


class Run(models.Model):
    STATUS_INIT = 'init'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_FINISHED = 'finished'

    STATUS_CHOICES = [
        (STATUS_INIT, 'Init'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_FINISHED, 'Finished'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    athlete = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='runs'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_INIT,
    )

    def __str__(self):
        return f"Run #{self.id} | Athlete: {self.athlete.username} | Status: {self.status}"


class AthleteInfo(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='athlete_info'
    )
    goals = models.TextField(blank=True)
    weight = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"AthleteInfo #{self.id} | User: {self.user.username}"


class Challenge(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(
        max_length=255,
        default="Сделай 10 забегов!"
    )
    athlete = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='challenges'
    )

    def __str__(self):
        return f"Challenge #{self.id} | Title: {self.title} | Athlete: {self.athlete.username}"


class Position(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    run = models.ForeignKey(
        Run,
        on_delete=models.CASCADE,
        related_name='positions'
    )

    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Position {self.id} | Run {self.run_id}"

