from django import forms

from .models import Organization, App

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'})
        }

class AppForm(forms.ModelForm):

    class Meta:
        model = App
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'})
        }
