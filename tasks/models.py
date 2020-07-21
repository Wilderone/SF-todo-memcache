from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    slug = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    todos_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.slug})'


class PriorChoice(models.Model):
    priority = models.CharField(default='High', max_length=15)

    def __str__(self):
        return self.priority


class PriorCount(models.Model):
    priority_counter = models.TextField(
        blank=True, default="{HI:0, ME:0, LO:0}")


class TodoItem(models.Model):
    # PRIORITY_HIGH = 1
    # PRIORITY_MEDIUM = 2
    # PRIORITY_LOW = 3

    # PRIORITY_CHOICES = [
    #     (PRIORITY_HIGH, "Высокий приоритет"),
    #     (PRIORITY_MEDIUM, "Средний приоритет"),
    #     (PRIORITY_LOW, "Низкий приоритет"),
    # ]

    # class Priority(models.TextChoices):
    #     PRIORITY_HIGH = 'HI', _('Высокий приоритет')
    #     PRIORITY_MEDIUM = 'ME', _('Средний приоритет')
    #     PRIORITY_LOW = 'LO', _('Низкий приоритет')

    description = models.TextField("описание")
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    # priority = models.CharField(
    #     "Приоритет", choices=Priority.choices, default=Priority.PRIORITY_MEDIUM, max_length=2
    # )
    priority = models.ForeignKey(
        PriorChoice, default=1, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])
