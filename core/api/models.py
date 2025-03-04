from django.db import models
from django.contrib.postgres.fields import ArrayField


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  # Name of application or job
    username = models.CharField(max_length=255) #username of the applicant
    data = models.JSONField()  # JSON field for additional data
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the application is created

    def __str__(self):
        return self.name