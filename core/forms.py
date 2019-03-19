from django import forms
from .models import Group, Set, Key, Backup, Survey, Guide, SurveyUser, SurveyDevice, SurveyServer, SurveyWorkStation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'slug',
        ]

        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        Layout(
            PrependedText('password', '@', placeholder="password", autocomplete='off')
        )
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(
            Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


class SetForm(forms.ModelForm):
    class Meta:
        model = Set

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'group',
            'slug',
        ]

        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
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
            'name': 'Name',
            'username': '',
            'password': '',
            'note': '',
            'url': '',
            'file': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
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


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'set',
            'slug',
        ]

        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(
            Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


class BackupForm(forms.ModelForm):
    class Meta:
        model = Backup

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'set',
            'slug',
        ]


        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'set',
            'slug',
        ]

        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


class SurveyUserForm(forms.ModelForm):
    class Meta:
        model = SurveyUser

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'survey',
            'slug',
        ]

        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


class SurveyWorkStationForm(forms.ModelForm):
    class Meta:
        model = SurveyWorkStation

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'survey',
            'slug',
        ]

        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


class SurveyServerForm(forms.ModelForm):
    class Meta:
        model = SurveyServer

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'survey',
            'slug',
        ]

        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))


class SurveyDeviceForm(forms.ModelForm):
    class Meta:
        model = SurveyDevice

        exclude = [
            'created_by',
            'last_modified_at',
            'created_at',
            'last_modified_by',
            'survey',
            'slug',
        ]

        labels = {

        }

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Accept'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="window.history.back()"))

