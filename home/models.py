from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.db.models import JSONField

class Organization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    ORGANIZATION_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=ORGANIZATION_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.name

class OrganizationUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    ORGANIZATION_USER_STATUS = (
        ('active', 'Active'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=ORGANIZATION_USER_STATUS,
        blank=False,
        default='active',
    )

    ORGANIZATION_USER_ROLE = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(
        max_length=25,
        choices=ORGANIZATION_USER_ROLE,
        blank=False,
        default='active',
    )

class App(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    APP_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=APP_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.name


class AppUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    app = models.ForeignKey('App', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    PROJECT_USER_STATUS = (
        ('active', 'Active'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=PROJECT_USER_STATUS,
        blank=False,
        default='active',
    )

    APP_USER_ROLE = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(
        max_length=25,
        choices=APP_USER_ROLE,
        blank=False,
        default='active',
    )

class Menu(models.Model):
    name = models.CharField(max_length=200)
    app = models.ForeignKey('App', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField()

    MENU_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=MENU_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.name

class List(models.Model):
    name = models.CharField(max_length=200)
    app = models.ForeignKey('App', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    fields = JSONField()

    LIST_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=LIST_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.name
