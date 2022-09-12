from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel


class TrackRecommendation(BaseModel):
    user_from = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="track_recommendation_from")
    user_to = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="track_recommendation_to")
    spotify_track_id = models.CharField(max_length=128)
    has_listened = models.BooleanField(default=False)

    class Meta:
        verbose_name = "track recommendations"
        verbose_name_plural = "track recommendations"
