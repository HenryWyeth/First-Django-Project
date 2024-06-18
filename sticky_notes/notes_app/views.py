from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm, TaskForm
from .models import Task


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                try:
                    user = User.objects.get(username=username)
                    messages.error(request,
                                   'Incorrect password. Please try again.')
                except User.DoesNotExist:
                    messages.error(request,
                                   'Username does not exist. Please try again or register.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    # Fetch tasks based on status
    not_started_tasks = Task.objects.filter(status='Not Started')
    on_track_tasks = Task.objects.filter(status='On Track')
    at_risk_tasks = Task.objects.filter(status='At Risk')
    overdue_tasks = Task.objects.filter(status='Overdue')
    complete_tasks = Task.objects.filter(status='Complete')

    return render(request, 'home.html', {
        'not_started_tasks': not_started_tasks,
        'on_track_tasks': on_track_tasks,
        'at_risk_tasks': at_risk_tasks,
        'overdue_tasks': overdue_tasks,
        'complete_tasks': complete_tasks,
    })


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.updated_by = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


@login_required
def view_task(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'view_task.html', {'task': task})


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('view_task', task_id=task_id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'update_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')
