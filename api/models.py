from django.db import models
from typing import List, Tuple

STATES: List[Tuple[str, str]] = [
    ('to-do', 'To Do'),
    ('in-progress', 'In Progress'),
    ('done', 'Done')
]


class Tasker(models.Model):

    task = models.TextField()
    state = models.CharField(choices=STATES, default=STATES[0], max_length=20)
    activity = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.task
