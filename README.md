# PROJECT REPORT: GAMIFIED DEEP WORK & SELF-IMPROVEMENT TRACKER


**Python Web Development with Django **  
**(Academic Session: 2025-26)**

---

## 1. ABOUT THE PROJECT

This project is a **Gamified Discipline and Productivity System** developed using the **Django** framework. Unlike traditional task managers, this system treats personal growth as a real-life RPG (Role-Playing Game).

It allows users to log daily effort across five core pillars of discipline:
1.  **Deep Work:** Focused coding and professional practice.
2.  **Academic:** Theoretical study and active learning.
3.  **Body:** Physical health, workouts, and eye care.
4.  **Mind:** Meditation, journaling, and reading.
5.  **Real Life:** Social confidence and creative output.

The system features a retro 8-bit aesthetic inspired by classic dungeon crawlers, integrating advanced frontend visualizations like an **HTML5 Canvas Radar Chart** and **SVG-based vector character sprites**.

---

## 2. OBJECTIVE OF THE PROJECT

*   To develop a web-based discipline tracking system using Django.
*   To implement a sophisticated leveling logic based on overall score (XP) and consistency (active days).
*   To integrate real-time UI updates using AJAX (Fetch API) for immediate feedback loops.
*   To visualize character growth through a dynamic hexagonal radar chart (Stats Hexagon).
*   To manage historical data through a color-scaled activity grid.
*   To design a modern "Vibe-driven" 8-bit UI using Vanilla CSS and custom vectors.

---

## 3. CODE / IMPLEMENTATION

### 3.1 URL Configuration (`tracker/urls.py`)
### **[PLACEHOLDER: INSERT SCREENSHOT OF tracker/urls.py HERE]**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('stats/', views.stats_view, name='stats'),
    path('history/', views.history_view, name='history'),
    path('api/complete_task/', views.complete_task_api, name='complete_task_api'),
]
```

### 3.2 Data Models (`tracker/models.py`)
### **[PLACEHOLDER: INSERT SCREENSHOT OF tracker/models.py HERE]**
```python
class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    total_xp = models.IntegerField(default=0)

    @property
    def xp_percentage(self):
        # Progress within the current 130-point bracket
        return (self.total_xp % 130) / 1.30

class Stat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strength = models.IntegerField(default=1)
    focus = models.IntegerField(default=1)
    knowledge = models.IntegerField(default=1)
    wisdom = models.IntegerField(default=1)
    confidence = models.IntegerField(default=1)
    creativity = models.IntegerField(default=1)
```

---



## 6. CONCLUSION

*   The **Gamified Deep Work Tracker** was successfully developed using the Django MVT architecture.
*   The project demonstrates the power of combining robust backend logic with high-performance Vanilla JS micro-interactions.
*   It successfully bridges the gap between productivity software and game design to encourage long-term habit formation.
*   **Future Scope:** Addition of social leaderboards, multiplayer boss battles, and a mobile-responsive "Companion App" for logging tasks on the go.
