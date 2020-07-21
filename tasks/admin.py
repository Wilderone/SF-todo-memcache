from django.contrib import admin

from tasks.models import TodoItem, Category, PriorChoice


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description',  'is_completed', 'created')
    exclude = ['priority_counter']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


@admin.register(PriorChoice)
class PriorityChoice(admin.ModelAdmin):
    pass
