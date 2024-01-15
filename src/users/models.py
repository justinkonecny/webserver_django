from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, UniqueConstraint

from base.models import BaseModel


def get_user_friends(self):
    # query for all friends of this user
    from_me = User.objects.filter(
        Q(friend_to__user_from=self)
    )
    to_me = User.objects.filter(
        Q(friend_from__user_to=self)
    )
    return from_me.union(to_me).all()


def get_active_group(self, **kwargs):
    member_of = self.groups_member_of.filter(is_active=True, **kwargs)
    created = self.created_groups.filter(is_active=True, **kwargs)
    return member_of.union(created).get()


def get_active_groups(self, **kwargs):
    member_of = self.groups_member_of.filter(is_active=True, **kwargs)
    created = self.created_groups.filter(is_active=True, **kwargs)
    return member_of.union(created).all()


User.add_to_class("get_friends", get_user_friends)
User.add_to_class("get_active_group", get_active_group)
User.add_to_class("get_active_groups", get_active_groups)


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
