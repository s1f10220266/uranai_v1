from django.db import models
from django.utils import timezone

# Create your models here.
class Scenario(models.Model):
    job = models.CharField(max_length=15)
    mbti = models.CharField(max_length=15)
    scenario = models.TextField()
    generated_at = models.DateTimeField(default=timezone.now)
    
    def generate(self):
        self.generated_at = timezone.now()
        self.save()
