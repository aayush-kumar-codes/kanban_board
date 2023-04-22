from django.db import models

from user.models import User


class Board(models.Model):
    user = models.ForeignKey(to=User)
    name = models.CharField(verbose_name="Board Name", max_length=25)
