from django.db import models
from django.contrib.postgres.fields import JSONField

class QueryLog(models.Model):
    query = models.TextField()
    tone = models.CharField(max_length=50)
    intent = models.CharField(max_length=50)
    suggested_actions = models.JSONField() 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query[:30]} - {self.tone} - {self.intent}"
