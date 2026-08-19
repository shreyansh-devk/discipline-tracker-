from django.contrib import admin
from .models import Character, Stat, DailyLog, Task, TaskCompletion, Achievement, UserAchievement

admin.site.register(Character)
admin.site.register(Stat)
admin.site.register(DailyLog)
admin.site.register(Task)
admin.site.register(TaskCompletion)
admin.site.register(Achievement)
admin.site.register(UserAchievement)