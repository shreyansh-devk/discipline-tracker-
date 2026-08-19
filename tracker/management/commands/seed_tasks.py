from django.core.management.base import BaseCommand
from tracker.models import Task, Category

class Command(BaseCommand):
    help = 'Seeds the database with default tasks'

    def handle(self, *args, **kwargs):
        tasks_to_create = [
            # Deep Work
            {"name": "Coding - Learning (Intent/Notes)", "category": Category.DEEP_WORK, "points": 5, "is_tiered": False},
            {"name": "Coding - 10 minutes", "category": Category.DEEP_WORK, "points": 3, "is_tiered": True},
            {"name": "Coding - 30 minutes", "category": Category.DEEP_WORK, "points": 8, "is_tiered": True},
            {"name": "Coding - 1 hour+", "category": Category.DEEP_WORK, "points": 18, "is_tiered": True},
            
            # Academic
            {"name": "Grazed material", "category": Category.ACADEMIC, "points": 5, "is_tiered": True},
            {"name": "Read material", "category": Category.ACADEMIC, "points": 10, "is_tiered": True},
            {"name": "Active interaction", "category": Category.ACADEMIC, "points": 15, "is_tiered": True},
            {"name": "Deep work (most done)", "category": Category.ACADEMIC, "points": 15, "is_tiered": True},
            {"name": "Deep work (all done)", "category": Category.ACADEMIC, "points": 20, "is_tiered": True},

            # Body
            {"name": "Stretching", "category": Category.BODY, "points": 2.5, "is_tiered": False},
            {"name": "Eye exercise", "category": Category.BODY, "points": 2.5, "is_tiered": False},
            {"name": "Workout", "category": Category.BODY, "points": 10, "is_tiered": False},
            {"name": "Stairs", "category": Category.BODY, "points": 2, "is_tiered": True},
            {"name": "Light walk", "category": Category.BODY, "points": 5, "is_tiered": True},
            {"name": "Proper cardio", "category": Category.BODY, "points": 10, "is_tiered": True},

            # Mind
            {"name": "Meditation", "category": Category.MIND, "points": 10, "is_tiered": False},
            {"name": "Journal", "category": Category.MIND, "points": 5, "is_tiered": False},
            {"name": "Read 1 page", "category": Category.MIND, "points": 5, "is_tiered": True},
            {"name": "Read 10 minutes", "category": Category.MIND, "points": 10, "is_tiered": True},
            {"name": "Read Entire chapter", "category": Category.MIND, "points": 15, "is_tiered": True},

            # Real Life
            {"name": "Talking head video", "category": Category.REAL_LIFE, "points": 10, "is_tiered": False},
            {"name": "Practice content", "category": Category.REAL_LIFE, "points": 10, "is_tiered": False},
            {"name": "Eye contact", "category": Category.REAL_LIFE, "points": 7, "is_tiered": True},
            {"name": "Ask stranger something", "category": Category.REAL_LIFE, "points": 2, "is_tiered": True},
            {"name": "Small conversation", "category": Category.REAL_LIFE, "points": 5, "is_tiered": True},
            {"name": "Proper full conversation", "category": Category.REAL_LIFE, "points": 10, "is_tiered": True},
        ]

        for t in tasks_to_create:
            task, created = Task.objects.get_or_create(
                name=t['name'],
                category=t['category'],
                defaults={'points': t['points'], 'is_tiered': t['is_tiered']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created task: {task.name}"))
            else:
                self.stdout.write(f"Task already exists: {task.name}")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
