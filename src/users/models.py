from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, UniqueConstraint

from base.models import BaseModel


def get_user_friends(self):
    # query for all friends of this user
    return User.objects.filter(
        Q(friend_to__user_from=self) |
        Q(friend_from__user_to=self)
    )


User.add_to_class("get_friends", get_user_friends)


class UserFriend(BaseModel):
    user_from = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="friend_from")
    user_to = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="friend_to")

    class Meta:
        verbose_name = "user friend"
        verbose_name_plural = "user friends"
        constraints = [
            UniqueConstraint(
                fields=["user_from", "user_to"],
                name="unique_friends_constraint",
            ),
            UniqueConstraint(
                fields=["user_to", "user_from"],
                name="unique_friends_rev_constraint",
            )
        ]
