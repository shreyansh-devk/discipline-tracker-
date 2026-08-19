# Gamified Deep Work & Self-Improvement Tracker
## Project Presentation & Technical Walkthrough

---

### 1. The Core Vision
The goal of this project was to build a **structured personal discipline system** disguised as an 8-bit retro RPG. Instead of a standard to-do list, this is a character-building game driven entirely by real-world actions across five pillars: Deep Work, Academics, Body, Mind, and Real Life.

**The Tech Stack:**
*   **Backend:** Django (Python), SQLite
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript, Custom SVG (No heavy frontend frameworks)

---

### 2. Initial Setup & Architecture
The foundation of the project relies on Django's **MVT (Model-View-Template)** architecture.

1.  **Project Initialization:** I started by scaffolding the Django project (`discipline_tracker`) and a core app (`tracker`) using `django-admin startproject` and `python manage.py startapp`.
2.  **Configuring the Environment:** I wired up the app in `settings.py`, configuring the template directories and static file paths so the app could serve CSS and HTML seamlessly.

---

### 3. Designing the Database Schema (Models)
The game engine requires a robust relational database. In `tracker/models.py`, I designed the following schema:
*   `User`: Standard Django authentication.
*   `Character`: Linked 1:1 to the User, tracking `level` and `total_xp`.
*   `Stat`: Linked 1:1 to the User, tracking specific RPG attributes (Strength, Focus, Knowledge, Wisdom, Confidence, Creativity).
*   `Task`: A master library of actionable items categorized by pillar, each with a specific point value.
*   `DailyLog` & `TaskCompletion`: Relational tables to track exactly what a user did on a specific day.

*Action Taken: I ran `python manage.py makemigrations` and `migrate` to translate these Python classes into SQLite tables.*

---

### 4. Seeding the Game Data
To make the application instantly usable, the database needed the master list of tasks. 
Instead of manually entering data through the Admin panel, I wrote a custom Django management command (`tracker/management/commands/seed_tasks.py`).
*   By running `python manage.py seed_tasks`, the database was autonomously populated with 26 categorized tasks (e.g., "Coding - 1 hour+" -> 18 points, "Meditation" -> 10 points).

---

### 5. Building the Engine (Views & Gamification Logic)
The core logic resides in `tracker/views.py`.
1.  **The Dashboard View:** Fetches all tasks, groups them by category (Deep Work, Body, etc.), and checks the `DailyLog` to see which tasks the user has already completed today. It passes this context to the template.
2.  **The API Endpoint (`complete_task_api`):** I created a custom JSON endpoint to handle task completions asynchronously. When a task is checked, this view calculates the points, updates the `DailyLog`, increments the `Character`'s XP, and handles level-ups—returning the updated stats instantly to the frontend.

---

### 6. The User Interface (Templates & CSS)
The visual identity relies on a strict 3-zone layout defined in `templates/base.html`:
1.  **Left Nav:** System navigation.
2.  **Center Console:** The primary interaction zone (task lists).
3.  **Right Panel:** Persistent character display, Level, and XP Bar.

**Styling Rules (`style.css`):**
*   Imported retro fonts: `Press Start 2P` (headings) and `VT323` (body).
*   Enforced strict, flat colors and "pixelated" borders (no rounded corners).

---

### 7. The CampusQuest Integration (Leveling Up the Vibe)
To elevate the visual polish, I cloned and analyzed an open-source React project called **CampusQuest** and extracted its best design patterns, adapting them for our Django/Vanilla JS stack:

*   **Color Palette:** I replaced standard greys with CampusQuest's rich dungeon palette (`#1a1a2e` night sky backgrounds, `#363640` dungeon walls) and specific stat colors (Mana Blue, Health Red, XP Green, Gold).
*   **Quest Scroll Styling:** I applied CampusQuest's "Parchment Scroll" aesthetic to our Task Blocks using CSS linear gradients and simulated wooden scroll-bars (`--color-parchment` and `--color-wood`).
*   **Floating Text Micro-interactions:** I analyzed CampusQuest's React `FloatingText` component. I recreated this effect in vanilla JavaScript inside `dashboard.html`. Now, checking a task dynamically generates a golden "+X pt" text element that physically floats up and fades away.
*   **The Stats Radar Chart:** CampusQuest featured a beautiful Hexagon radar chart for stats. Because I couldn't use their React/SVG library directly, I reverse-engineered the trigonometry and rebuilt it entirely using the HTML5 `<canvas>` API in `stats.html`. It mathematically plots the user's STR, INT, WIS, etc., and draws a glowing, gradient-filled polygon.

---

### 8. The 8-Bit Vector Character
Finally, the user needed an avatar. While CampusQuest used raster `.png` sprite sheets, the requirement was a scalable vector graphic.
*   I hand-coded a raw SVG string directly into `base.html`. It mathematically plots an 8-bit RPG Knight (armor, helmet, sword, gold belt) on a 32x32 pixel grid. By applying the CSS rule `image-rendering: pixelated;`, the vector scales infinitely without blurring, maintaining the perfect retro aesthetic while keeping file sizes microscopic.

---

### Summary
By combining Django's robust backend architecture with highly optimized, vanilla frontend techniques and borrowing design language from modern React projects (CampusQuest), we successfully built a gamified, real-world RPG engine that is lightweight, responsive, and incredibly rewarding to use.