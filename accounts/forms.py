from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control form-control-solid'}))
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control form-control-solid'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-solid'
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-solid'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-solid'


class UpdateProfileForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control form-control-solid'}))
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control form-control-solid'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-solid'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-solid'
