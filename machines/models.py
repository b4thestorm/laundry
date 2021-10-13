import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

WASHING_MACHINES = 6
DRYERS = 8


class CustomUser(AbstractUser):
    username = models.CharField(max_length=500, default="")
    email = models.EmailField(_("email address"), unique=True)
    push_token = models.CharField(max_length=500, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            instance.username = instance.email
            instance.save()
            Token.objects.create(user=instance)


class Machine(models.Model):
    minutes = models.CharField(max_length=2)
    start_time = models.DateTimeField(default=datetime.datetime.now())
    number_of_machines = models.CharField(max_length=2)
    machine_type = models.CharField(max_length=50)
    expired = models.BooleanField(default=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)

    def set_expired(self):
        if self.expired:
            return True
        else:
            self.expired = True
            self.save()
        return True

    @classmethod
    def machines_remaining(cls):
        recent_dryers = cls.objects.filter(machine_type="dryers")
        expired_machines = len([dryer for dryer in recent_dryers if dryer.expired])
        available_dryers = 8 - expired_machines

        recent_washers = cls.objects.filter(machine_type="washers")
        expired_machines = len([washer for washer in recent_washers if washer.expired])
        available_washer_machines = 6 - expired_machines
        available_machine_count = {
            "available_dryers": available_dryers,
            "available_washer_machines": available_washer_machines,
        }
        return available_machine_count
