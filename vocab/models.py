from django.db import models

class Vocab(models.Model):
    word = models.TextField()
    total_fails = models.IntegerField(default=0)
    total_success = models.IntegerField(default=0)
    last_successive_successes = models.IntegerField(default=0)
    is_spelling = models.BooleanField(default=False)
    audio_url = models.TextField(null=True)

    
