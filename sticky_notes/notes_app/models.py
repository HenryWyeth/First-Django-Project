from django.db import models


# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str___(self):
        return self.username


class Task(models.Model):
    status_choices = [
        ('Not Started', 'Not Started'),
        ('On Track', 'On Track'),
        ('At Risk', 'At Risk'),
        ('Overdue', 'Overdue'),
        ('Complete', 'Complete'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.TextField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=status_choices)

    def __str__(self):
        return self.title
