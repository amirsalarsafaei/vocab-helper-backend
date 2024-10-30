from django.db import models
from datetime import timedelta

from django.utils.timezone import now


class Vocab(models.Model):
    word = models.TextField()
    total_fails = models.IntegerField(default=0)
    total_success = models.IntegerField(default=0)
    last_successive_successes = models.IntegerField(default=0)
    is_spelling = models.BooleanField(default=False)
    audio_url = models.TextField(null=True)
    def get_default_last_answered():
        return now() - timedelta(hours=3)
    
    last_answered = models.DateTimeField(default=get_default_last_answered)

    def correct_answer(self):
        self.last_answered = now()
        self.total_success += 1
        self.last_successive_successes += 1

    

    def incorrect_answer(self):
        self.total_fails += 1
        self.last_successive_successes = 0
