from django.shortcuts import render, redirect, get_object_or_404 # <<
from django.http import HttpResponse 
from .models import ToDoItem, Event # <<
from django.forms.models import model_to_dict # <<
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import AddEventForm

# s04
from django.contrib.auth.hashers import make_password
from . forms import LoginForm, AddTaskForm, UpdateTaskForm, RegisterForm, AddEventForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='todolist:login')
def index(request): 
    todoitem_list = ToDoItem.objects.filter(user_id=request.user.id)
    event_list = Event.objects.filter(user_id=request.user.id)

    context = {
        'todoitem_list': todoitem_list,
        'event_list': event_list,
        'user': request.user,  # Add this line
    }
    return render(request, "todolist/index.html", context)


def todoitem(request, todoitem_id):
    todoitem = get_object_or_404(ToDoItem, pk=todoitem_id)
    return render(request, "todolist/todoitem.html", {"todoitem": todoitem, "user": request.user})

def register(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if not form.is_valid():

            form = RegisterForm()

        else:
            # form.cleaned_data comes from the HTML form input values 
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            duplicates = User.objects.filter(email=email)
            
            if not duplicates and password == confirm_password:
                User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=make_password(password), is_staff=False, is_active=True)
                return redirect("todolist:login")

            else:
                context = {
                    "error": True
                }

    return render(request, "todolist/register.html", context)

def change_password(request):
    is_user_authenticated = False
    user = authenticate(username="johndoe", password="johndoe1")

    print(user)
    if user is not None:
        authenticated_user = User.objects.get(username='johndoe')
        authenticated_user.set_password("john1234")
        # authenticated_user.first_name = "john john john john"
        authenticated_user.save()
        is_user_authenticated = True
    context = {
        "is_user_authenticated": is_user_authenticated
    }

    return render(request, "todolist/change_password.html", context)

def login_view(request):
    # Initialize an empty context dictionary for template rendering
    context = {}

    # Check if the request is a POST (form submission)
    if request.method == 'POST':

        # Bind form data to the LoginForm (with validation)
        form = LoginForm(request.POST)

        # If the form is invalid, reinitialize an empty form
        if form.is_valid() == False:

            form = LoginForm()

        else:
            # Extract validated form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Attempt to authenticate the user
            user = authenticate(username=username, password=password)
            
            context = {
                "username": username,
                "password": password
            }
            
            # If user credentials are correct
            if user is not None:
                login(request, user)
                return redirect("todolist:index")
            else:
                # Set error flag to display error in template
                context = {
                    "error": True
                }

    return render(request, "todolist/login.html", context) # << update# << update# << update

def logout_view(request):
	# clear session cookie that is associated with login
    logout(request)
    return redirect("todolist:index") # << s04

# ------------ s04 CRUD TODOLIST --------------------

def add_task(request):
    context = {}
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if not form.is_valid():
            return render(request, "todolist/add_task.html", {"form": form})

        else:
            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']
            duplicates = ToDoItem.objects.filter(task_name=task_name)
            if not duplicates:
                ToDoItem.objects.create(task_name=task_name, description=description, date_created=timezone.now(), user_id=request.user.id)
                # Redirect to the homepage after successful task creation
                return redirect("todolist:index")
            else:
                # If duplicate exists, pass an error message to the context
                context = {
                    "error": True
                }

    return render(request, "todolist/add_task.html", context)

# View for updating a task
def update_task(request, todoitem_id):

    # Retrieve the ToDoItem using its primary key
    todoitem = ToDoItem.objects.filter(pk=todoitem_id)

    context = {
        "user": request.user,
        "todoitem_id": todoitem_id,
        "task_name": todoitem[0].task_name,
        "description": todoitem[0].description,
        "status": todoitem[0].status
    }

    # Check if the request method is POST
    if request.method == 'POST':

        # Create a form instance with the submitted data
        form = UpdateTaskForm(request.POST)

        if form.is_valid() == False:

            form = UpdateTaskForm()

        else:
             # Extract cleaned/validated data from the form
            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']
            
            if todoitem:
                # If the ToDoItem exists, update its values
                todoitem[0].task_name = task_name
                todoitem[0].description = description
                todoitem[0].status = status

                # Save changes to the database
                todoitem[0].save()
                return redirect("todolist:index")

            else:
                # If task was not found, update context to show an error
                context = {
                    "error": True
                }

    return render(request, "todolist/update_task.html", context)

def delete_task(request, todoitem_id):

    todoitem = ToDoItem.objects.filter(pk=todoitem_id).delete()
    return redirect("todolist:index")

@login_required(login_url='todolist:login')
def add_event(request):
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.status = "pending" 
            event.save()
            return redirect("todolist:index") 
    else:
        form = AddEventForm()

    return render(request, "todolist/add_event.html", {"form": form})


@login_required(login_url='todolist:login')
def event(request, event_id):
    event_obj = get_object_or_404(Event, pk=event_id, user=request.user)
    return render(request, "todolist/event.html", {"event": event_obj})


@login_required(login_url='todolist:login')
def update_event(request, event_id):
    event_obj = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == "POST":
        form = AddEventForm(request.POST, instance=event_obj)
        if form.is_valid():
            form.save()
            return redirect("todolist:index")
    else:
        form = AddEventForm(instance=event_obj)

    return render(request, "todolist/update_event.html", {"form": form, "event": event_obj})


@login_required(login_url='todolist:login')
def delete_event(request, event_id):
    event_obj = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == "POST":  # confirm deletion
        event_obj.delete()
        return redirect("todolist:index")

    return render(request, "todolist/delete_event.html", {"event": event_obj})