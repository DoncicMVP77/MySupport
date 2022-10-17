from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Ticket(models.Model):
    Status = (
        ("Open", "Open"),
        ("Froze", "Froze"),
        ("Close", "Close"),
        )

    Category = (
        ("Account", "Account"),
        ("Storage", "Storage"),
        ("Market Place", "Market Place"),
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=225, unique=True, db_index=True, verbose_name="URL")
    category = models.CharField("Category of ticket", max_length=50, choices=Category)
    title = models.CharField("Subject", max_length=50, blank=True)
    description = models.TextField("Description of question or issue")
    timestamp = models.DateTimeField(default=(datetime.now()))
    last_activity = models.DateTimeField(auto_now=True)
    status = models.CharField("Status of ticket", max_length=30, choices=Status, default="Open")


    def get_absolute_url(self):
        return reverse("ticket_create", kwargs={"post_slug": self.slug})


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(default=(datetime.now()))
