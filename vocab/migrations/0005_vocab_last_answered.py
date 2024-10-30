# Generated by Django 5.1.2 on 2024-10-30 09:25

import vocab.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0004_vocab_audio_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='vocab',
            name='last_answered',
            field=models.DateTimeField(default=vocab.models.Vocab.get_default_last_answered),
        ),
    ]