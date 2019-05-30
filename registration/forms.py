from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Key, Note, Guide
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required 254 characters or fewer. Letters, digits and @/./+/-/_ only.")
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_superuser", "is_staff")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email) is None:
            raise forms.ValidationError("Email exists, try with other.")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = [
            'avatar',
            'birthday',
            'job',
        ]

        labels = {
            'avatar': 'avatar',
            'birthday': 'birthday',
            'email': 'email',
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Required 254 characters or fewer. Letters, digits and @/./+/-/_ only.")

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email exists, try with other.")
        return email


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note

        fields = [
            'name',
            'note',
        ]

        labels = {
            'name': '',
            'note': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            #'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'note-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(
            Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide

        fields = [
            'name',
            'guide',
            'file',
        ]

        labels = {
            'name': '',
            'guide': '',
            'file': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'guide': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guide'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'guide-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(
            Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))



class KeyForm(forms.ModelForm):
    class Meta:
        model = Key

        fields = [
            'name',
            'username',
            'password',
            'note',
            'url',
            'file',
        ]

        labels = {
            'name': '',
            'username': '',
            'password': '',
            'note': '',
            'url': '',
            'file': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'key-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(
            Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))
