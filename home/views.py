from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Organization, OrganizationUser, App, AppUser
from .forms import OrganizationForm, AppForm

#===============================================================================
# Static Pages
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


def archive_organization(request, organization_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)

    organization.status = "archived"
    organization.save()

    return redirect('organizations')

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


def edit_app(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.method == "POST":
        form = AppForm(request.POST, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
            app.last_updated = timezone.now()
            app.save()
            return redirect('app_details', organization_pk=organization_pk, app_pk=app_pk)
    else:
        form = AppForm(instance=app)
        context = {
            'form': form,
            'organization': organization,
            'app': app
        }
        return render(request, 'home/app-form.html', {'form': form})


def archive_app(request, organization_pk, app_pk):

    app = get_object_or_404(App, pk=app_pk)

    app.status = "archived"
    app.save()

    return redirect('apps', organization_pk=organization_pk)


@login_required
def app_details(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    #Lists should go here at some point
    context = {
        'organization': organization,
        'app': app
    }

    return render(request, 'home/app-details.html', context=context)


#===============================================================================
# App
#===============================================================================

@login_required
def activity(request):

    html = loader.render_to_string(
        'home/activity.html'
    )
    # package output data and return it as a JSON object
    output_data = {
        'html': html
    }
    return JsonResponse(output_data)

@login_required
def tasks(request):

    html = loader.render_to_string(
        'home/tasks.html'
    )
    # package output data and return it as a JSON object
    output_data = {
        'html': html
    }
    return JsonResponse(output_data)

@login_required
def lists(request):

    html = loader.render_to_string(
        'home/lists.html'
    )
    # package output data and return it as a JSON object
    output_data = {
        'html': html
    }
    return JsonResponse(output_data)

# ------------------------------------------------

def ajaxSample(request):

    if request.is_ajax and request.method == "POST":
        name = request.POST.get('name', 'empty')
        print("Request to create organization " + name)

        return redirect('organization_details', organization_pk="123456789")
        #return redirect('organization_details', organization_pk="123456789")

    else:

        name = request.POST.get('name', 'empty')
        print("Request to create organization " + name)

        context = {}
