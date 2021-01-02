from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('about/', views.about, name='about'),

    path('organizations/', views.organizations, name='organizations'),
    path('organizations/add/', views.add_organization, name='add_organization'),
    path('organizations/<int:organization_pk>/settings', views.organization_settings, name='organization_settings'),
    path('organizations/<int:organization_pk>/edit', views.edit_organization, name='edit_organization'),
    path('organizations/<int:organization_pk>/archive', views.archive_organization, name='archive_organization'),

    path('organizations/<int:organization_pk>/apps/', views.apps, name='apps'),
    path('organizations/<int:organization_pk>/apps/add/', views.add_app, name='add_app'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/', views.app_details, name='app_details'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/settings', views.app_settings, name='app_settings'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/edit', views.edit_app, name='edit_app'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/archive', views.archive_app, name='archive_app'),

    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/', views.lists, name='lists'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/create-list/', views.create_list, name='create_list'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/save-list/', views.save_list, name='save_list'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>', views.list, name='list'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/edit', views.edit_list, name='edit_list'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/update', views.update_list, name='update_list'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/settings', views.list_settings, name='list_settings'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/archive', views.archive_list, name='archive_list'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/add-record', views.add_record, name='add_record'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/save-record', views.save_record, name='save_record'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/records/<int:record_pk>/', views.record, name='record'), # Forward without details to details
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/records/<int:record_pk>/details', views.record_details, name='record_details'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/records/<int:record_pk>/notes', views.record_notes, name='record_notes'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/records/<int:record_pk>/tasks', views.record_tasks, name='record_tasks'),
    path('organizations/<int:organization_pk>/apps/<int:app_pk>/lists/<int:list_pk>/records/<int:record_pk>/edit', views.edit_record, name='edit_record'),

    path('organizations/<int:organization_pk>/apps/<int:app_pk>/notes/', views.notes, name='notes'),

    path('organizations/<int:organization_pk>/apps/<int:app_pk>/dashboard/', views.dashboard, name='dashboard'),

    path('organizations/<int:organization_pk>/apps/<int:app_pk>/tasks/', views.tasks, name='tasks'),




]
