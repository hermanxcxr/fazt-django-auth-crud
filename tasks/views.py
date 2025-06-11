from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login #crea la cookie
from django.contrib.auth import logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import TaskForm
from .models import Tasks
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm()})
    elif request.method == "POST":        
        if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = User.objects.create_user(
                        username=request.POST["username"],
                        password=request.POST["password1"],                
                    )
                    user.save() #
                    login(request, user) # crea la cookie de sesion
                    return redirect ("tasks")
                except IntegrityError:
                    # Si el usuario ya existe, se lanza una excepción IntegrityError
                    # y se muestra un mensaje de error en la plantilla signup.html
                   return render(request, "signup.html", 
                                 {"form": UserCreationForm(),
                                  "error": "Username already exists. Please choose a different username."
                                  })                
        else:
            return render(request, "signup.html", 
                                 {"form": UserCreationForm(),
                                  "error": "Passwords do not match. Please try again."
                                  }) 

@login_required
def tasks(request):
    tasks = Tasks.objects.filter(user=request.user, datecompleted__isnull=True) # filtra las tareas por el usuario logueado
    return render(request, "tasks.html",{'tasks':tasks})

@login_required
def tasks_completed(request):
    tasks = Tasks.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, "tasks.html",{'tasks':tasks})

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm()})
    elif request.method == "POST":
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "create_task.html", {"form": TaskForm(), 'error': 'Bad data passed in. Try again.'})

@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Tasks, pk=task_id, user=request.user)   #Tasks.objects.get(pk=task_id)
        form = TaskForm(instance=task) # crea un formulario con la tarea
        return render(request, "task_detail.html", {
            'task': task,
            'form': form,
        })
    else:
        try:
            task = get_object_or_404(Tasks, pk=task_id, user=request.user) #Tasks.objects.get(pk=task_id, user=request.user) 
            #UPDATE
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
             return render(request, "task_detail.html", {
            'task': task,
            'form': form,
            'error': 'Bad info passed in. Try again.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now() # marca la tarea como completada
        task.save()
        return redirect("tasks")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == "POST":        
        task.delete()
        return redirect("tasks")

@login_required
def signout(request):
    logout(request) # elimina la cookie de sesion
    return redirect("home") # redirige a la pagina de inicio

def signin(request):
    if request.method == 'GET':
        return render(request, "signin.html",{'form': AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "signin.html",{'form': AuthenticationForm(),'error': 'Username and password do not match.'})
        else:
            login(request, user) # guarda la cookie de sesion
            return redirect("tasks")
        

