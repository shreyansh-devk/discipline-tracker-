from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="character")
    level = models.IntegerField(default=1)
    total_xp = models.IntegerField(default=0)
    
    # Appearance placeholders
    hair_style = models.CharField(max_length=50, default="default")
    clothing_color = models.CharField(max_length=50, default="neutral")
    skin_tone = models.CharField(max_length=50, default="neutral")

    def __str__(self):
        return f"{self.user.username}'s Character (Lvl {self.level})"

    @property
    def xp_percentage(self):
        # Progress within the current 130-point bracket
        return (self.total_xp % 130) / 1.30  # Same as (val / 130) * 100

    @property
    def xp_within_level(self):
        return self.total_xp % 130

class Stat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stats")
    strength = models.IntegerField(default=1)     # Body
    focus = models.IntegerField(default=1)        # Deep Work
    knowledge = models.IntegerField(default=1)    # Academic
    wisdom = models.IntegerField(default=1)       # Mind
    confidence = models.IntegerField(default=1)   # Real Life (Cold Approach)
    creativity = models.IntegerField(default=1)   # Real Life (Video)

    def __str__(self):
        return f"{self.user.username}'s Stats"

@receiver(post_save, sender=User)
def create_user_character_and_stats(sender, instance, created, **kwargs):
    if created:
        Character.objects.create(user=instance)
        Stat.objects.create(user=instance)

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_logs")
    date = models.DateField(auto_now_add=True)
    total_points = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Category(models.TextChoices):
    DEEP_WORK = 'DW', 'Deep Work'
    ACADEMIC = 'AC', 'Academic'
    BODY = 'BO', 'Body'
    MIND = 'MI', 'Mind'
    REAL_LIFE = 'RL', 'Real Life'

class Task(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=Category.choices)
    points = models.FloatField()
    is_tiered = models.BooleanField(default=False)
    # Tiered tasks might just be distinct Task entries, e.g. "Coding - 10 min", "Coding - 30 min".
    # For simplicity, we can just represent them as separate Task items in the DB, 
    # but group them in the UI.

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name} ({self.points} pts)"

class TaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_completions")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    log = models.ForeignKey(DailyLog, on_delete=models.CASCADE, related_name="completions")
    timestamp = models.DateTimeField(auto_now_add=True)
    points_earned = models.FloatField()

    def __str__(self):
        return f"{self.user.username} completed {self.task.name} at {self.timestamp}"

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="default_icon") # Reference to SVG class or filename
    
    # Simple logic storage (e.g. "total_xp >= 100", "days_streak >= 7")
    # For a robust system, we would evaluate conditions in python. 
    # We can use an identifier to hook up specific python logic.
    condition_identifier = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} unlocked {self.achievement.name}"