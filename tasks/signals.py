import json

from django.db.models.signals import m2m_changed, post_delete, post_save

from django.dispatch import receiver
from tasks.models import TodoItem, Category, PriorChoice, PriorCount
from collections import Counter


def prior_calc():
    # Благодаря введению отдельной табицы для приоритетов можно
    priorities = {}
    for prior_name in PriorChoice.objects.all():
        priorities[prior_name.priority] = 0
    for prior in TodoItem.objects.all():
        priorities[prior.priority.priority] += 1
    PriorCount.objects.create(priority_counter=json.dumps(priorities))


def count_calc():
    cat_counter = Counter()
    print("count calc")
    for todo in TodoItem.objects.all():
        for cat in todo.category.all():
            cat_counter[cat.slug] += 1

    # Если в списке категорий у задач отсутствует существующая категория - в счетчике ей присваивается значение 0
    for allcat in Category.objects.all():
        if allcat.slug not in cat_counter.keys():
            cat_counter[allcat.slug] = 0

    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)

    prior_calc()


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):

    if action != 'post_add':
        return

    count_calc()


@receiver(post_delete, sender=TodoItem)
def task_cats_removed(sender, instance, **kwargs):

    count_calc()


@receiver(post_save, sender=TodoItem)
def priority_count_add(sender, instance, **kwargs):
    prior_calc()
