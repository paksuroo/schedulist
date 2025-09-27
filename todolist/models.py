from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ToDoItem(models.Model):
	task_name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	# description = models.CharField(max_length=200, blank=True, null=True)
	status = models.CharField(max_length=50, default ="pending")
	# 'date created' is a human-readable label shown in admin or forms
	date_created = models.DateTimeField("date created")

	user = models.ForeignKey(User, on_delete=models.CASCADE, default="") # << s04

class Event(models.Model):
	event_name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	status = models.CharField(max_length=50, default ="pending")
	event_date = models.DateTimeField("event date")
	user = models.ForeignKey(User, on_delete=models.CASCADE, default="")