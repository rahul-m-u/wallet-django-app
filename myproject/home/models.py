import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    customer_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

