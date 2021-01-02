from django import forms
from django.forms import formset_factory, modelformset_factory

from .models import Organization, App

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name','description',)

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control form-control-solid'}),
            'description': forms.TextInput(attrs={'class':'form-control form-control-solid'})
        }

class AppForm(forms.ModelForm): #(Workspaces)

    class Meta:
        model = App
        fields = ('name','description',)

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control form-control-solid'}),
            'description': forms.TextInput(attrs={'class':'form-control form-control-solid'})
        }
