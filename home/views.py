from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.core import serializers

from .models import Organization, OrganizationUser, App, AppUser, Menu, List
from .forms import OrganizationForm, AppForm

#===============================================================================
# Static Pages / Home Page Setup
#===============================================================================

def home(request):
    context = {}
    return render(request, 'home/home.html', context=context)

def terms(request):
    context = {}
    return render(request, 'home/terms.html', context=context)

def privacy(request):
    context = {}
    return render(request, 'home/privacy.html', context=context)

def about(request):
    context = {}
    return render(request, 'home/about.html', context=context)

#===============================================================================
# Organizations
#===============================================================================

@login_required
def organizations(request):
    userOrganizations = OrganizationUser.objects.filter(user=request.user, status__exact='active', organization__status__exact="active").order_by('organization__name',)
    organizations = []
    for userOrganization in userOrganizations:
        organizations.append(userOrganization.organization)

    context = {
        'organizations': organizations
    }

    return render(request, 'home/organizations.html', context=context)

@login_required
def add_organization(request):

    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():

            # Save the new project
            organization = form.save(commit=False)
            organization.created_user = request.user
            organization.created_at = timezone.now()
            organization.save()

            # Save the new user <> project relation
            organizationUser = OrganizationUser()
            organizationUser.user = request.user
            organizationUser.organization = organization
            organizationUser.status = "active"
            organizationUser.role = "admin"
            organizationUser.save()

            return redirect('apps', organization_pk=organization.pk)

    else:
        form = OrganizationForm()

        return render(request, 'home/organization-form.html', {'form': form})

@login_required
def edit_organization(request, organization_pk):
    organization = get_object_or_404(Organization, pk=organization_pk)

    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.last_updated = timezone.now()
            organization.save()
            return redirect('organizations')
    else:
        form = OrganizationForm(instance=organization)

        context = {
            'organization': organization,
            'form': form
        }

        return render(request, 'home/organization-form.html', {'form': form})

@login_required
def archive_organization(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)

    organization.status = "archived"
    organization.save()

    return redirect('organizations')

@login_required
def organization_settings(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)

    form = OrganizationForm(instance=organization)

    context = {
        'organization': organization,
        'form': form
    }

    return render(request, 'home/organization-settings.html', context=context)

#===============================================================================
# Apps (Workspaces)
#===============================================================================

@login_required
def apps(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    userApps = AppUser.objects.filter(user=request.user, status__exact='active', app__status__exact="active", app__organization=organization).order_by('app__name',)
    apps = []
    for userApp in userApps:
        apps.append(userApp.app)

    context = {
        'organization': organization,
        'apps': apps
    }

    return render(request, 'home/apps.html', context=context)

@login_required
def add_app(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)

    if request.method == "POST":
        form = AppForm(request.POST)
        if form.is_valid():

            # Save the new project
            app = form.save(commit=False)
            app.organization = organization
            app.created_user = request.user
            app.created_at = timezone.now()
            app.save()

            # Save the new user <> project relation
            appUser = AppUser()
            appUser.user = request.user
            appUser.app = app
            appUser.status = "active"
            appUser.role = "admin"
            appUser.save()

            return redirect('app_details', organization_pk=organization_pk, app_pk=app.pk)

    else:

        form = AppForm()
        context = {
            'form': form,
            'organization': organization
        }

        return render(request, 'home/app-form.html', {'form': form})

@login_required
def edit_app(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.method == "POST":
        form = AppForm(request.POST, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
            app.last_updated = timezone.now()
            app.save()
            return redirect('apps', organization_pk=organization_pk)
    else:
        form = AppForm(instance=app)

        context = {
            'organization': organization,
            'app': app,
            'form': form
        }

        return render(request, 'home/app-form.html', {'form': form})

@login_required
def archive_app(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    app.status = "archived"
    app.save()

    return redirect('apps', organization_pk=organization_pk)

@login_required
def app_settings(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    form = AppForm(instance=app)

    context = {
        'organization': organization,
        'app': app,
        'form': form
    }

    return render(request, 'home/app-settings.html', context=context)

@login_required
def app_details(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    context = {
        'organization': organization,
        'app': app,
        'type': 'dashboard'
    }

    return render(request, 'home/workspace.html', context=context)

#===============================================================================
# Menus
#===============================================================================

@login_required
def add_menu(request, organization_pk, app_pk):

    if request.is_ajax and request.method == "POST":

        organization = get_object_or_404(Organization, pk=organization_pk)
        app = get_object_or_404(App, pk=app_pk)
        menu_name = request.POST.get('menu_name', None)

        menu = Menu.objects.create(
            name=menu_name,
            app=app,
            status='active',
            order=0,
            created_at = timezone.now(),
            created_user=request.user)
        menu.save();

        menus = Menu.objects.all().order_by('order').filter(status='active', app=app);

        html = render_to_string(
            template_name="home/menu-list.html",
            context={
                'organization': organization,
                'app': app,
                'menus': menus
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

def edit_menu(request, organization_pk, app_pk, menu_pk):

    if request.is_ajax and request.method == "POST":

        name = request.POST.get('menu_name', 'empty')
        menu = get_object_or_404(Menu, pk=menu_pk)
        menu.name = name
        menu.save()

        menus = Menu.objects.all().order_by('order').filter(status='active', app=app);

        html = render_to_string(
            template_name="home/menu-list.html",
            context={
                'organization': organization,
                'app': app,
                'menus': menus
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

def archive_menu(request, organization_pk, app_pk, menu_pk):

    if request.is_ajax and request.method == "POST":

        menu = get_object_or_404(Menu, pk=menu_pk)

        manu.status = "archived"
        menu.save()

        menus = Menu.objects.all().order_by('order').filter(status='active', app=app);

        html = render_to_string(
            template_name="home/menu-list.html",
            context={
                'organization': organization,
                'app': app,
                'menus': menus
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)


#===============================================================================
# Workspace Pages
#===============================================================================

@login_required
def dashboard(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax() and request.method == "GET":

        html = render_to_string(
            template_name="home/dashboard.html",
            context={
                'organization': organization,
                'app': app
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'type': 'dashboard'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def tasks(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax() and request.method == "GET":

        html = render_to_string(
            template_name="home/tasks.html",
            context={
                'organization': organization,
                'app': app
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'type': 'tasks'
        }

        return render(request, 'home/workspace.html', context=context)


@login_required
def notes(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax() and request.method == "GET":

        html = render_to_string(
            template_name="home/notes.html",
            context={
                'organization': organization,
                'app': app
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'type': 'notes'
        }

        return render(request, 'home/workspace.html', context=context)


#===============================================================================
# Lists
#===============================================================================

@login_required
def lists(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    lists = List.objects.all().filter(status='active', app=app)

    if request.is_ajax() and request.method == "GET":

        html = render_to_string(
            template_name="home/lists.html",
            context={
                'organization': organization,
                'app': app,
                'lists': lists
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'lists': lists,
            'type': 'lists'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    if request.is_ajax() and request.method == "GET":

        html = render_to_string(
            template_name="home/list.html",
            context={
                'organization': organization,
                'app': app,
                'list': list
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'type': 'list'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def create_list(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    lists = List.objects.all().filter(status='active', app=app)

    if request.is_ajax() and request.method == "GET":

        html = render_to_string(
            template_name="home/list-create.html",
            context={
                'organization': organization,
                'app': app
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'type': 'list-create'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def edit_list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    lists = List.objects.all().filter(status='active', app=app)

    if request.is_ajax() and request.method == "GET":

        html = render_to_string(
            template_name="home/list-create.html",
            context={
                'organization': organization,
                'app': app,
                'list_id': list.id
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'list_id': list.id,
            'type': 'edit-list'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def list_details(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    if request.is_ajax() and request.method == "GET":

        # Get the list details required for editing
        list_details = {}
        list_details['name'] = list.name
        list_details['fields'] = list.fields

        return JsonResponse(data=list_details, safe=False)


@login_required
def save_list(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax and request.method == "POST":

        list_name = request.POST.get('list_name', None)

        field_list = json.loads(request.POST['fields'])

        list = List.objects.create(
            name=list_name,
            app=app,
            status='active',
            created_at=timezone.now(),
            created_user=request.user,
            fields=field_list)
        list.save();

        # TODO Return page redirect
        data_dict = {"message": "Success"}

        return JsonResponse(data=data_dict, safe=False)

@login_required
def update_list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    if request.is_ajax and request.method == "POST":

        list_name = request.POST.get('list_name', None)

        field_list = json.loads(request.POST['fields'])

        list.name=list_name
        list.last_updated = timezone.now()
        list.fields = field_list
        list.save();

        # TODO Return page redirect
        data_dict = {"message": "Success"}

        return JsonResponse(data=data_dict, safe=False)

@login_required
def archive_list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    list.status = "archived"
    list.save()

    return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)

@login_required
def list_settings(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    context = {
        'organization': organization,
        'app': app,
        'list': list
    }

    return render(request, 'home/list-settings.html', context=context)

@login_required
def add_record(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    if request.is_ajax() and request.method == "GET":

        html = render_to_string(
            template_name="home/add-record.html",
            context={
                'organization': organization,
                'app': app,
                'list': list
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'type': 'add-record'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def save_record(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    print(request.POST)

    # TODO Return page redirect
    data_dict = {"message": "Success"}

    return JsonResponse(data=data_dict, safe=False)
