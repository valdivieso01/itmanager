from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm, NoteForm, KeyForm, GuideForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, TemplateView
from .models import Profile, Note, Key, Guide ,storage1
from private_storage.views import PrivateStorageView
from django.http import HttpResponseRedirect, Http404


class Login(TemplateView):
    template_name = "registration/login.html"


class UserCreate(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('user_list') + '?register'

    def get_form(self, form_class=None):
        form = super(UserCreate, self).get_form()
        form.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Username'})
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Email'})
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Password'})
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Repeat password'})
        return form


class UserList(ListView):
    model = User
    template_name = 'registration/user_list.html'

    def get_queryset(self):
        return User.objects.all()


class UserDelete(DeleteView):
    model = User
    template_name = 'registration/user_confirm_delete.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = User.objects.filter(username=self.kwargs['username'])

        if not queryset:
            raise Http404

        context = {'user': self.kwargs['username']}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = User.objects.filter(username=self.kwargs['username'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('user_list') + '?deleted'


class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        # recuperar o crear el objeto que se va a editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # recuperar el objeto que se va a editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificiar en tiempo real
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Email'})
        return form


# Items

class MyStorageView1(PrivateStorageView):
    storage = storage1

    def can_access_file(self, private_file):
        user_name = self.request.path.split('/')
        if self.request.user.username == user_name[2]:
            return self.request
        else:
            raise PermissionDenied

class KeyDetail(DetailView):
    model = Key

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Key.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user):
            queryset = Key.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user)

        if not queryset:
            raise Http404

        return queryset


class KeyList(ListView):
    model = Key

    def get_queryset(self):
        if self.request.GET:
            return  Key.objects.filter(profile__user=self.request.user, name__icontains=self.request.GET['q'])
        else:
            return  Key.objects.filter(profile__user=self.request.user)


class KeyCreate(CreateView):
    model = Key
    form_class = KeyForm


    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('key_list')


class KeyUpdate(UpdateView):
    form_class = KeyForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return Key.objects.filter(profile__user=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Key.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user):
            queryset = Key.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user)

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('key_list')


class KeyDelete(DeleteView):
    model = Key

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = Key.objects.filter(slug=self.kwargs['slug']).filter(profile__user=self.request.user)

        if not queryset:
            raise Http404

        context = {'key': self.kwargs['slug']}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = Key.objects.filter(slug=self.kwargs['slug']).filter(profile__user=self.request.user)
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('key_list')


class NoteDetail(DetailView):
    model = Note

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Note.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user):
                queryset = Note.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user)

        if not queryset:
            raise Http404

        return queryset


class NoteList(ListView):
    model = Note

    def get_queryset(self):
        if self.request.GET:
            return Note.objects.filter(profile__user=self.request.user, name__icontains=self.request.GET['q'])
        else:
            return Note.objects.filter(profile__user=self.request.user)

class NoteCreate(CreateView):
    model = Note
    form_class = NoteForm

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('note_list')


class NoteUpdate(UpdateView):
    form_class = NoteForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return Note.objects.filter(profile__user=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Note.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user):
            queryset = Note.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user)

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('note_list')


class NoteDelete(DeleteView):
    model = Note

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = Note.objects.filter(slug=self.kwargs['slug']).filter(profile__user=self.request.user)

        if not queryset:
            raise Http404

        context = {'note': self.kwargs['slug']}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = Note.objects.filter(slug=self.kwargs['slug']).filter(profile__user=self.request.user)
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('note_list')


class GuideDetail(DetailView):
    model = Guide

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Guide.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user):
                queryset = Guide.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user)

        if not queryset:
            raise Http404

        return queryset


class GuideList(ListView):
    model = Guide

    def get_queryset(self):
        if self.request.GET:
            return  Guide.objects.filter(profile__user=self.request.user, name__icontains=self.request.GET['q'])
        else:
            return Guide.objects.filter(profile__user=self.request.user)


class GuideCreate(CreateView):
    model = Guide
    form_class = GuideForm

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('guide_list')


class GuideUpdate(UpdateView):
    form_class = GuideForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return Note.objects.filter(profile__user=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Guide.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user):
            queryset = Guide.objects.get(slug=self.kwargs['slug'], profile__user=self.request.user)

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('guide_list')


class GuideDelete(DeleteView):
    model = Guide

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = Guide.objects.filter(slug=self.kwargs['slug']).filter(profile__user=self.request.user)

        if not queryset:
            raise Http404

        context = {'guide': self.kwargs['slug']}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = Guide.objects.filter(slug=self.kwargs['slug']).filter(profile__user=self.request.user)
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('guide_list')

