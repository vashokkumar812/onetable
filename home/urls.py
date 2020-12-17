from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('about/', views.about, name='about'),

    path('organizations/', views.organizations, name='organizations'),
    path('organizations/add/', views.add_organization, name='add_organization'),
    path('organizations/<int:organization_pk>/edit', views.edit_organization, name='edit_organization'),
    path('organizations/<int:organization_pk>/archive', views.archive_organization, name='archive_organization'),

    path('organizations/<int:organization_pk>/apps/', views.apps, name='apps'),
    path('organizations/<int:organization_pk>/apps/add/', views.add_app, name='add_app'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/', views.app_details, name='app_details'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/edit', views.edit_app, name='edit_app'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/archive', views.archive_app, name='archive_app'),

    path('organizations/<int:organization_pk>/apps/<int:app_pk>/activity/', views.activity, name='activity'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/tasks/', views.tasks, name='tasks'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/', views.lists, name='lists'),

]
