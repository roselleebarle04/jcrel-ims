from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ExpandedUser(AbstractUser):
    address = models.CharField(max_length=50, blank=True)
    #prof_pic = models.ImageField('avatar', upload_to = 'avatar', null = True, blank = True)
