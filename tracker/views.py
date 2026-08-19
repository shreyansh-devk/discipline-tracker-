import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from .models import Task, DailyLog, TaskCompletion, Category

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('character_setup')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def character_setup(request):
    # Setup character customization later
    return redirect('dashboard')

@login_required
def dashboard(request):
    tasks = Task.objects.all()
    
    # Get or create today's log
    today = date.today()
    log, created = DailyLog.objects.get_or_create(user=request.user, date=today)
    
    # Get completed task IDs for today to pre-check checkboxes
    completed_task_ids = TaskCompletion.objects.filter(log=log).values_list('task_id', flat=True)
    
    # Group tasks by category
    grouped_tasks = {
        Category.DEEP_WORK: tasks.filter(category=Category.DEEP_WORK),
        Category.ACADEMIC: tasks.filter(category=Category.ACADEMIC),
        Category.BODY: tasks.filter(category=Category.BODY),
        Category.MIND: tasks.filter(category=Category.MIND),
        Category.REAL_LIFE: tasks.filter(category=Category.REAL_LIFE),
    }
    
    context = {
        'grouped_tasks': grouped_tasks,
        'completed_task_ids': list(completed_task_ids),
        'daily_points': log.total_points,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
@csrf_exempt
def complete_task_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        is_completed = data.get('is_completed')
        
        try:
            task = Task.objects.get(id=task_id)
            today = date.today()
            log, _ = DailyLog.objects.get_or_create(user=request.user, date=today)
            char = request.user.character
            
            if is_completed:
                # Add completion
                TaskCompletion.objects.create(
                    user=request.user,
                    task=task,
                    log=log,
                    points_earned=task.points
                )
                log.total_points += task.points
                char.total_xp += task.points
                
                # Update specific Stats
                stats = request.user.stats
                if task.category == Category.BODY:
                    stats.strength += task.points
                elif task.category == Category.DEEP_WORK:
                    stats.focus += task.points
                elif task.category == Category.ACADEMIC:
                    stats.knowledge += task.points
                elif task.category == Category.MIND:
                    stats.wisdom += task.points
                elif task.category == Category.REAL_LIFE:
                    # Distinguish between Creativity (Video) and Confidence (Social)
                    if "video" in task.name.lower() or "content" in task.name.lower():
                        stats.creativity += task.points
                    else:
                        stats.confidence += task.points
                stats.save()
            else:
                # Remove completion (if exists)
                completion = TaskCompletion.objects.filter(user=request.user, task=task, log=log).first()
                if completion:
                    log.total_points -= task.points
                    char.total_xp -= task.points
                    
                    # Deduct from Stats
                    stats = request.user.stats
                    if task.category == Category.BODY:
                        stats.strength -= task.points
                    elif task.category == Category.DEEP_WORK:
                        stats.focus -= task.points
                    elif task.category == Category.ACADEMIC:
                        stats.knowledge -= task.points
                    elif task.category == Category.MIND:
                        stats.wisdom -= task.points
                    elif task.category == Category.REAL_LIFE:
                        if "video" in task.name.lower() or "content" in task.name.lower():
                            stats.creativity -= task.points
                        else:
                            stats.confidence -= task.points
                    stats.save()
                    completion.delete()
                    
            log.save()
            char.save()
            
            # Enhanced Leveling Logic
            # Base Level from total XP (130 threshold)
            xp_level = int(char.total_xp // 130)
            
            # Consistency Bonus: 1 level per 5 active days
            active_days = DailyLog.objects.filter(user=request.user, total_points__gt=0).count()
            consistency_bonus = int(active_days // 5)
            
            new_level = xp_level + consistency_bonus + 1
            
            if new_level != char.level:
                char.level = new_level
                char.save()
                
            return JsonResponse({
                'status': 'success',
                'daily_points': log.total_points,
                'total_xp': char.total_xp,
                'xp_within_level': char.xp_within_level,
                'level': char.level,
                'xp_percentage': char.xp_percentage
            })
            
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def stats_view(request):
    return render(request, 'tracker/stats.html')

@login_required
def history_view(request):
    logs = DailyLog.objects.filter(user=request.user).order_by('-date')
    # Add intensity for template scaling (0.1 to 1.0)
    for log in logs:
        log.intensity = min(0.1 + (log.total_points / 100), 1.0)
    return render(request, 'tracker/history.html', {'logs': logs})

@login_required
def day_detail_api(request, log_id):
    try:
        log = DailyLog.objects.get(id=log_id, user=request.user)
        completions = log.completions.all()
        data = {
            'date': log.date.strftime('%Y-%m-%d'),
            'total_points': log.total_points,
            'tasks': [{'name': c.task.name, 'points': c.points_earned} for c in completions]
        }
        return JsonResponse(data)
    except DailyLog.DoesNotExist:
        return JsonResponse({'error': 'Log not found'}, status=404)

@login_required
def achievements_view(request):
    return render(request, 'tracker/achievements.html')

@login_required
def settings_view(request):
    return render(request, 'tracker/settings.html')