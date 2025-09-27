from django.urls import path
from . import views

app_name = 'todolist'

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:todoitem_id>/", views.todoitem, name="viewtodoitem"),

    # Auth
    path('register', views.register, name="register"),
    path('change_password', views.change_password, name="change_password"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),

    # Task CRUD
    path('add_task', views.add_task, name="add_task"),
    path('<int:todoitem_id>/edit', views.update_task, name='update_task'),
    path('<int:todoitem_id>/delete', views.delete_task, name='delete_task'),

    # Event CRUD
    path('add_event', views.add_event, name="add_event"),
    path('event/<int:event_id>/', views.event, name="event"), 
    path('event/<int:event_id>/update', views.update_event, name='update_event'),
    path('event/<int:event_id>/delete', views.delete_event, name='delete_event'),
]
