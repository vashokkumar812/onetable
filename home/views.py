from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.core import serializers
import uuid
import random
import string
from django.core import serializers
from .models import Organization, OrganizationUser, App, AppUser, Menu, List, ListField, Record, RecordField, RecordRelation,RecordComment
from .forms import OrganizationForm, AppForm, ListForm, ListFieldFormset, TaskForm, NoteForm

# TODO
# On all views, @login_required prevents users not logged in, but need method and
# approach for making sure users are viewing / editing / creating / etc. only in
# the apps and organizations they have been added to and (eventually) have the
# correct permissions for.


# TODO
# Urls for template / page rendering and ajax are mixed in together, messy and
# hard to organize. Need to split somehow into ajax/ url or organize so it's clear
# which url routes are used for ajax, and what is used for page template rendering



#===============================================================================
# Static Pages / Home Page Setup
#===============================================================================

def home(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/home.html', context=context)

def terms(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/terms.html', context=context)

def privacy(request):
    # Placeholder for now
    context = {}
    return render(request, 'home/privacy.html', context=context)

def about(request):
    # Placeholder for now
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

    # Uses standard django forms

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

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)

    if request.method == "POST":
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save(commit=False)
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

    # Uses standard django forms

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

    # Uses standard django forms

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

    # Uses standard django forms

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.method == "POST":
        form = AppForm(request.POST, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
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

    # Uses standard django forms

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

    # Always loads the full workspace here (no ajax), defaults to dashboard content
    # in the template file
    return render(request, 'home/workspace.html', context=context)


#===============================================================================
# Workspace Pages
#===============================================================================

@login_required
def dashboard(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

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

        # If accessing the url directly, load full page

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

        # Call is ajax, just load main content needed here

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

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'type': 'tasks'
        }

        return render(request, 'home/workspace.html', context=context)


#===============================================================================
# Lists
#===============================================================================

@login_required
def lists(request, organization_pk, app_pk):
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    # lists = List.objects.all().filter(status='active', app=app)
    lists = List.objects.filter(status='active', app=app).order_by('name',)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

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

        # If accessing the url directly, load full page

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

    records = Record.objects.all().filter(status='active', list=list)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/list.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'records': records
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:
        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'records': records,
            'type': 'list'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def create_list(request, organization_pk, app_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)

    # Django formset stuff

    # Use model formset and not inline formset for more control over the data
    # being saved (i.e. setting and checking primary fields, etc.)

    if request.method == 'GET':
        listform = ListForm(request.GET or None)
        formset = ListFieldFormset(queryset=List.objects.none())
        # Reduce the queryset for select_list field to just active lists in current app
        for form in formset:
            form.fields['select_list'].queryset = List.objects.filter(app=app, status='active')

    elif request.method == 'POST':
        listform = ListForm(request.POST)
        formset = ListFieldFormset(request.POST)

        # Verify the form submitted is valid
        if listform.is_valid() and formset.is_valid():
            list = listform.save(commit=False)
            list.app = app
            list.created_user = request.user
            list.created_at = timezone.now()
            list.save() # Save here then update primary field once field is saved
            # Loop through the list field forms submitted
            list_field_order = 0
            change_from_select_list = False
            for index, form in enumerate(formset):
                # Save the list field
                list_field = form.save(commit=False)
                list_field.field_id = randStr(N=10)
                list_field.list = list
                list_field.created_user = request.user
                list_field.created_at = timezone.now()
                list_field.order = list_field_order

                if index == 0:
                    list_field.primary = True
                    list_field.required = True
                    list_field.visible = True

                list_field.save()
                list_field.field_id = list_field.id
                list_field.save()

                for select_list_id in request.POST.getlist(f'form-{index}-select_list'):
                    if form.cleaned_data.get('select_list') is not None:
                        if int(select_list_id) != int(form.cleaned_data.get('select_list').id):
                            ListField.objects.create(
                                created_at=timezone.now(),
                                created_user=request.user,
                                list=list,
                                field_label=request.POST[f'form-{index}-field_label'],
                                field_type=request.POST[f'form-{index}-field_type'],
                                select_list_id=int(select_list_id),
                                order=list_field_order
                            )

                            list_field_order += 1
                            change_from_select_list = True

                if change_from_select_list is False:
                    list_field_order += 1

            return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)
        else:
            print(formset.errors)

    context={
        'organization': organization,
        'app': app,
        'listform': listform,
        'formset': formset,
        'type': 'list-create'
    }

    # TODO eventually handle ajax calls vs. direct link call

    return render(request, 'home/workspace.html', context=context)

@login_required
def edit_list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    # Django formset stuff

    # Use model formset and not inline formset for more control over the data
    # being saved (i.e. setting and checking primary fields, etc.)

    if request.method == 'GET':
        listform = ListForm(request.GET or None, instance=list)
        formset = ListFieldFormset(queryset=ListField.objects.filter(list=list, status='active').order_by('order'))
        # Reduce the queryset for select_list field to just active lists in current app
        for form in formset:
            form.fields['select_list'].queryset = List.objects.filter(app=app, status='active')

    elif request.method == 'POST':
        listform = ListForm(request.POST, instance=list)
        formset = ListFieldFormset(data=request.POST)

        # Verify the form submitted is valid
        if listform.is_valid() and formset.is_valid():

            list = listform.save(commit=False)
            list.updated_at = timezone.now()
            list.save() # Save here then update primary field once field is saved
            # Loop through the list field forms submitted
            list_field_order = 0
            for index, form in enumerate(formset):
                if int(index) != int(request.POST.get('form-INITIAL_FORMS')):
                # Save the list field
                    list_field = form.save()
                    list_field.list = list
                    list_field.updated_at = timezone.now()
                    list_field.created_user = request.user
                    list_field.order = list_field_order
                    if list_field.order == 0:
                        list_field.primary = True
                        list_field.required = True
                        list_field.visible = True
                    list_field.save()

                    list_field_order += 1

            remove_list_field_ids = request.POST.getlist('delete_list_field_ids')
            for list_field_id in remove_list_field_ids:
                try:
                    list_field_object = ListField.objects.get(id=int(list_field_id))
                    list_field_object.status = "deleted"
                    list_field_object.save()
                except: pass
            return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)
        else:
            print(f'List Form Error\t\t\t\t{listform.errors}\nField Type Error\t\t\t\t{formset.errors}')

    context={
        'organization': organization,
        'app': app,
        'listform': listform,
        'formset': formset,
        'type': 'edit-list'
    }

    # TODO eventually handle ajax calls vs. direct link call

    return render(request, 'home/workspace.html', context=context)


@login_required
def archive_list(request, organization_pk, app_pk, list_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    list.status = "archived"
    list.save()

    # Able to use a redirect here because we did a direct POST request
    return redirect('lists', organization_pk=organization_pk, app_pk=app_pk)

@login_required
def list_settings(request, organization_pk, app_pk, list_pk):

    # Does not / will not use the standard django forms per the comments noted
    # above

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    context = {
        'organization': organization,
        'app': app,
        'list': list
    }

    return render(request, 'home/list-settings.html', context=context)


#===============================================================================
# Records
#===============================================================================
@login_required
def add_record(request, organization_pk, app_pk, list_pk):
    # Very similar to the edit_record view, but includes the field values previously saved
    # Probably a way to combine these views to consolidate

    # We are not using the following here:
    # 1) Django form.Forms (couldn't find a way to create dynamic forms this approach,
    # but we may be able to find eventually)
    # 2) the models.Model @property for list.list_fields or the record.record_fields >>
    # needed an object with both the field inforation and value included so we can edit previous values here

    # Instead, only approach could find is building an object here then passing it to the frontend
    # template for rending the form

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    fields = []
    for list_field in list.list_fields:
        field_object = {}
        field_object['field_id'] = list_field.field_id
        field_object['field_label'] = list_field.field_label
        field_object['field_type'] = list_field.field_type
        field_object['required'] = list_field.required
        field_object['primary'] = list_field.primary
        field_object['visible'] = list_field.visible
        field_object['order'] = list_field.order
        field_object['id'] = list_field.id
        if list_field.field_type == "choose-from-list":
            field_object['select_record'] = RecordField.objects.filter(record__list=list_field.select_list.id, record__status="active", status="active", list_field__primary=True).values_list('record', 'value')
        fields.append(field_object)
    fields.reverse()

    if request.is_ajax() and request.method == "GET":
        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-create.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'fields': fields
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:
        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'fields': fields,
            'type': 'edit-record',
        }

        return render(request, 'home/workspace.html', context=context)


@login_required
def save_record(request, organization_pk, app_pk, list_pk):

    # This handles both saving and updating a record

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    record_id = request.POST.get('record_id', None)
    fields = json.loads(request.POST['field_values'])

    print('==========================record id', record_id)
    print('==========================fields', fields)

    # TODO
    # Needs error handling here verify if the form is valid (i.e. all required fields, acceptable data types, etc)

    record = None # Create object globally outside of the if/else

    if record_id is not None:
        print('=================here')
        # Get the existing record / this is a record being edited
        record = get_object_or_404(Record, pk=record_id)
        print('==============record', record)
    else:
        # Add a new record
        record = Record.objects.create(
            list=list,
            status='active',
            created_at=timezone.now(),
            created_user=request.user)
        record.save()

    for field in fields:
            print('============================field', field)
            if field['fieldValue']:
            # if field['fieldValue'] is not None:
                # Only save a RecordField object if there is a value

                if record_id is not None:
                    try:
                        print('==================in try')
                        # Update existing record field
                        # TODO only update if the value changed
                        record_field = RecordField.objects.get(status='active', list_field__field_id=field['fieldId'], record=record)
                        if field['fieldType'] == "choose-from-list":
                           record_field.selected_record_id = field['fieldValue']
                           record_field.value = field['selectListValue']
                        else:
                            record_field.value = field['fieldValue']
                        record_field.save()

                        # Update existing relationship
                        if field['fieldType'] == "choose-from-list":
                            try:
                                record_relation = RecordRelation.objects.get(status='active', list_field__field_id=field['fieldId'], parent_record=record)
                                record_relation.child_record_id = field['fieldValue']
                                record_relation.save()
                            except RecordRelation.DoesNotExist:
                                # Create the record relation / does not exist
                                record_relation = RecordRelation.objects.create(
                                    parent_record=record,
                                    child_record_id=record_field.selected_record_id,
                                    relation_type='choose-from-list',
                                    list_field=record_field.list_field,
                                    status='active',
                                    created_at=timezone.now(),
                                    created_user=request.user)
                                record_relation.save()

                    except RecordField.DoesNotExist:
                        print('=================in execpt')
                        # This record field has not been saved before, so create it
                        # TODO this is redundant with below / can be consolidated eventually
                        try:

                            list_field = ListField.objects.get(status='active', field_id=field['fieldId'], list=list)

                            # Create the new record field
                            record_field = RecordField.objects.create(
                                record=record,
                                list_field=list_field,
                                status='active',
                                created_at=timezone.now(),
                                created_user=request.user)
                            record_field.save()

                            if field['fieldType'] == "choose-from-list":
                                record_field.selected_record_id = field['fieldValue']
                                record_field.value = field['selectListValue']
                            else:
                                record_field.value = field['fieldValue']
                            record_field.save()

                            # Create the record relation if select from list
                            if field['fieldType'] == "choose-from-list":
                                record_relation = RecordRelation.objects.create(
                                    parent_record=record,
                                    child_record_id=record_field.selected_record_id,
                                    relation_type='choose-from-list',
                                    list_field=record_field.list_field,
                                    status='active',
                                    created_at=timezone.now(),
                                    created_user=request.user)
                                record_relation.save()

                        except ListField.DoesNotExist:
                            # Easy error handling for now
                            pass

                else:

                    try:

                        # Create new record field

                        list_field = ListField.objects.get(status='active', field_id=field['fieldId'], list=list)

                        record_field = RecordField.objects.create(
                            record=record,
                            list_field=list_field,
                            status='active',
                            created_at=timezone.now(),
                            created_user=request.user)
                        record_field.save()

                        if field['fieldType'] == "choose-from-list":
                            record_field.selected_record_id = field['fieldValue']
                            record_field.value = field['selectListValue']
                        else:
                            record_field.value = field['fieldValue']
                        record_field.save()

                        # Create the record relation if select from list
                        if field['fieldType'] == "choose-from-list":
                            record_relation = RecordRelation.objects.create(
                                parent_record=record,
                                child_record_id=record_field.selected_record_id,
                                relation_type='choose-from-list',
                                list_field=record_field.list_field,
                                status='active',
                                created_at=timezone.now(),
                                created_user=request.user)
                            record_relation.save()

                    except ListField.DoesNotExist:
                        # Easy error handling for now
                        pass

    # Using ajax here to save because cannot do a POST request and get the field values
    # from a dynamically created form (or at least I couldn't figure out how to
    # do this, although there may be a way to!)

    # Redirect based on ajax call from frontend on success

    data_dict = {"success": True}

    return JsonResponse(data=data_dict, safe=False)


@login_required
def record(request, organization_pk, app_pk, list_pk, record_pk):
    comments = RecordComment.objects.filter(record_id=record_pk).order_by('-pk')
    # Record details page (placeholder for now)
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)
    print(record.list.pk)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'record': record
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'type': 'record',
            'record_view': 'record-details',
            "comments":comments
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def record_details(request, organization_pk, app_pk, list_pk, record_pk):

    # Record details page (placeholder for now)

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)
    note_form = NoteForm()
    comments = RecordComment.objects.filter(record_id=record_pk).order_by('-pk')
    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here
        
        html = render_to_string(
            template_name="home/record-details.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'record': record,
                'note_form': note_form,
                

            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    # TODO add access here for direct link
    # For now just return record details
    if request.method == "GET":

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'note_form': note_form,
            'type': 'record',
            'record_view': 'record-details',
            "comments":comments
        }

        return render(request, 'home/workspace.html', context=context)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():

            # Save the new project
            note = form.save()

            context = {
                'organization': organization,
                'app': app,
                'list': list,
                'record': record,
                'note_form': note_form,
                'type': 'record',
                'record_view': 'record-details',
            }

            return render(request, 'home/workspace.html', context=context)

@login_required
def record_tasks(request, organization_pk, app_pk, list_pk, record_pk):

    # Record details page (placeholder for now)
    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)
    task_form = TaskForm()

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-tasks.html",
            context={
                'record': record,
                'task_form': task_form
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'task_form': task_form,
            'type': 'record',
            'record_view': 'record-tasks'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def record_links(request, organization_pk, app_pk, list_pk, record_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)

    # Record details page (placeholder for now)
    record = get_object_or_404(Record, pk=record_pk)
    record_relations = RecordRelation.objects.all().filter(status='active', child_record=record, parent_record__status='active')
    records = []
    for relation in record_relations:
        records.append(relation.parent_record)

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-links.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'record': record,
                'records': records

            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'records': records,
            'type': 'record',
            'record_view': 'record-links'
        }

        return render(request, 'home/workspace.html', context=context)

@login_required
def edit_record(request, organization_pk, app_pk, list_pk, record_pk):

    organization = get_object_or_404(Organization, pk=organization_pk)
    app = get_object_or_404(App, pk=app_pk)
    list = get_object_or_404(List, pk=list_pk)
    record = get_object_or_404(Record, pk=record_pk)

    # Very similar to the add_record view, but includes the field values previously saved
    # Probably a way to combine these views to consolidate

    # We are not using the following here:
    # 1) Django form.Forms (couldn't find a way to create dynamic forms this approach,
    # but we may be able to find eventually)
    # 2) the models.Model @property for list.list_fields or the record.record_fields >>
    # needed an object with both the field inforation and value included so we can edit prvious values here

    # Instead, only approach could find is building an object here then passing it to the frontend
    # template for rending the form

    fields = []
    for list_field in list.list_fields:

        field_object = {}
        field_object['field_id'] = list_field.field_id
        field_object['field_label'] = list_field.field_label
        field_object['field_type'] = list_field.field_type
        field_object['required'] = list_field.required
        field_object['primary'] = list_field.primary
        field_object['visible'] = list_field.visible
        field_object['order'] = list_field.order
        # Get the field value if it exists
        if list_field.field_type == "choose-from-list":
            field_object['select_record'] = RecordField.objects.filter(record__list=list_field.select_list.id, record__status="active", status="active", list_field__primary=True).values_list('record', 'value')
            try:
                field_object['value'] = RecordField.objects.get(record_id=record_pk, list_field_id=list_field.id, status="active").value
            except:
                pass
        else:
            for record_field in record.record_fields:
                if list_field.id == record_field.list_field.id:
                    field_object['value'] = record_field.value

        fields.append(field_object)
    fields.reverse()

    if request.is_ajax() and request.method == "GET":

        # Call is ajax, just load main content needed here

        html = render_to_string(
            template_name="home/record-create.html",
            context={
                'organization': organization,
                'app': app,
                'list': list,
                'fields': fields,
                'record': record
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    else:

        # If accessing the url directly, load full page

        context = {
            'organization': organization,
            'app': app,
            'list': list,
            'record': record,
            'fields': fields,
            'type': 'edit-record'
        }

        return render(request, 'home/workspace.html', context=context)

# TODO need view for archiving records
def archive_record(request, organization_pk, app_pk, list_pk, record_pk):
    #   this functional is call when user click on the "Archive Record" button on Record Detail Page
    record = get_object_or_404(Record, pk=record_pk)
    record.status = "archived"
    record.save()
    return redirect('list', organization_pk=organization_pk, app_pk=app_pk, list_pk=list_pk)

# TODO need view for create task, edit task, archive task, get tasks (will use
# standard django forms for this)

# TODO need view for create note, edit note, archive note, get notes (will use
# standard django forms for this)

#===============================================================================
# Records
#===============================================================================

# Will be used later for replacing the default django pk / id's in urls
def generate_random_string(string_length=10):
    # Not sure this is the best approach, but works okay for now

    random = str(uuid.uuid4()) # Make into string
    random = random.replace("-","") # Just letters and numbers
    return random[0:string_length] # Truncate to correct length

def randStr(chars = string.ascii_uppercase + string.ascii_lowercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))


def post_record_comment(request,organization_pk, app_pk, list_pk, record_pk):
    if request.method == "POST":
        if request.POST['content'] != '':
            record_comment = RecordComment(created_user=request.user,content = request.POST['content'],record_id=record_pk)
            record_comment.save()
            data_dict={}
        
            myarray = serializers.serialize("json", [record_comment],ensure_ascii=False)
            json=myarray[1:-1]
            return JsonResponse(data=json, safe=False)
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        return HttpResponse('Unauthorized', status=401)