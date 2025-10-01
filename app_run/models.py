from django.db import models


class User(models.Model):
    athlete = models.CharField(max_length=100)

    def __str__(self):
        return self.athlete


class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.athlete


