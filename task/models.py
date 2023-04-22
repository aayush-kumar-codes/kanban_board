from django.db import models

from user.models import User


class Board(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Board Name", max_length=25)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE)
    task_description = models.CharField(max_length=250)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(f"<Task: {self.id}>")
