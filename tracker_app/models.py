from django.db import models
from django.conf import settings


class Subject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    max_score = models.PositiveIntegerField(blank=True)

    def __str__(self):
        """
        Magic method is redefined to show all information about Subject.
        :return: subject id and theme
        """
        return f"{self.theme}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Subject class.
        :return: class, id
        """
        return f"{Subject.__name__}(id={self.id})"


class Task(models.Model):
    STATUS_CHOICES = (
        ('done', "Виконане"),
        ('processing', "В процесі"),
        ('scheduled', "Заплановане"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, verbose_name='subjects')
    name = models.CharField(max_length=256)
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField(editable=False, auto_now=True)
    deadline = models.DateTimeField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='scheduled')

    def __str__(self):
        """
        Magic method is redefined to show all information about Task.
        :return:  task id and name
        """
        return f"'id': {self.id}, 'name': '{self.name}'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Task class.
        :return: class, id
        """
        return f"{Task.__name__}(id={self.id})"
