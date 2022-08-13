from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class CorpusUp(models.Model):
    post_id = models.IntegerField(primary_key=True)
    vers = models.CharField(max_length=25)
    date = models.CharField(max_length=25)
    post = models.TextField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.post
