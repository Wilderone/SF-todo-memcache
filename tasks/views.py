import json
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.cache import cache_page
from tasks.models import TodoItem, Category, PriorChoice, PriorCount
from datetime import datetime


def index(request):

    # Final version
    counts = {c.name: c.todos_count for c in Category.objects.all()}
    priorities = json.loads(PriorCount.objects.last(
    ).priority_counter) if PriorCount.objects.last() else json.loads("{HI:0, ME:0, LO:0}")
    return render(request, "tasks/index.html", {"counts": counts, "priorities": priorities})

# 60 секунд * 5 = 5 минут. По мне так гораздо читабельней


@cache_page(60 * 5)
def cache_date(request):
    return render(request, "tasks/cach_date.html", {"date": datetime.now()})


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = []
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        # print(user_tasks)
        if len(user_tasks) == 0:
            context["categories"] = ['No Tasks']
            return context

        for t in user_tasks:
            # print(t)
            tags.append(t.category.all())

        categories = []
        # print('ALL CATS', tags)
        for cat in tags:
            # print('CAT', cat)
            if cat.first() not in categories:
                categories.append(cat.first())

        sorted_by_cats = {cat: [] for cat in categories}

        for todo in user_tasks:
            sorted_by_cats[todo.category.first()].append(todo)
        # print('CNTXT', context['tasks'][0].__dict__)
        context["categories"] = categories
        context["tasks"] = sorted_by_cats
        # print('result', context)
        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"
