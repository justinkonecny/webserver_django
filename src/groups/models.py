import uuid as uuid
from django.db import models
from django.contrib.auth.models import User

from base.models import BaseModel


def create_join_key():
    return uuid.uuid4().hex[:6].upper()


class Group(BaseModel):
    is_active = models.BooleanField(default=False)
    join_key = models.CharField(default=create_join_key, editable=False, max_length=16, unique=True)
    passcode = models.CharField(max_length=16, blank=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="created_groups")
    members = models.ManyToManyField(to=User, through="GroupMembership", related_name="groups_member_of")


class GroupTrack(BaseModel):
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, related_name="tracks")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    spotify_track_id = models.CharField(max_length=128)
    listened = models.BooleanField(default=False)


class GroupMembership(BaseModel):
    class GroupRole(models.TextChoices):
        FOLLOWER = ("FOL", "Follower")
        LEADER = ("LEA", "Leader")

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=3,
        choices=GroupRole.choices,
        default=GroupRole.FOLLOWER,
    )

    def is_leader(self):
        return self.role == self.GroupRole.LEADER

    def is_follower(self):
        return self.role == self.GroupRole.FOLLOWER

# def get_members(self):
#     # query for all friends of this user
#     from_me = User.objects.filter(
#         Q(friend_to__user_from=self)
#     )
#     to_me = User.objects.filter(
#         Q(friend_from__user_to=self)
#     )
#     return from_me.union(to_me).all()
#
#
# Group.add_to_class("get_friends", get_user_friends)
