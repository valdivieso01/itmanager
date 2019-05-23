from django.forms import forms
from django.http import HttpResponseRedirect, Http404
from django.views.generic.base import TemplateView
from private_storage.views import PrivateStorageView
from .models import Group, Set, Key, Backup, Survey, Guide, storage2, SurveyUser, SurveyWorkStation, SurveyServer, SurveyDevice
from .forms import GroupForm, SetForm, KeyForm, BackupForm, SurveyForm, GuideForm, SurveyUserForm, SurveyWorkStationForm, SurveyServerForm, SurveyDeviceForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

class HomePage(TemplateView):
    template_name = "core/home.html"

# Groups


class GroupList(ListView):
    model = Group

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)


class GroupDetail(DetailView):
    model = Group

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)


class GroupDelete(DeleteView):
    model = Group

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)

    def get_success_url(self):
        return reverse_lazy('group_list') + '?deleted'


class GroupCreate(CreateView):
    model = Group
    form_class = GroupForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('group_list') + '?created'


class GroupUpdate(UpdateView):
    form_class = GroupForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)

    def get_success_url(self):
        return reverse_lazy('group_list') + '?edited'


# Sets


class SetDetail(DetailView):
    model = Set

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Set.objects.get(slug=self.kwargs['set'], group__slug=self.kwargs['slug'], group__members=self.request.user):
            queryset = Set.objects.get(slug=self.kwargs['set'], group__slug=self.kwargs['slug'],
                                       group__members=self.request.user)

        if not queryset:
            raise forms.ValidationError("Set incorrect")

        return queryset


class SetUpdate(UpdateView):
    form_class = SetForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return Set.objects.filter(group__members=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Set.objects.get(slug=self.kwargs['set'], group__slug=self.kwargs['slug'], group__members=self.request.user):
            queryset = Set.objects.get(slug=self.kwargs['set'], group__slug=self.kwargs['slug'],
                                       group__members=self.request.user)

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('group_detail', args=[self.object.group.slug]) + '?edited'


class SetCreate(CreateView):
    model = Set
    form_class = SetForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        group_slug = self.kwargs['slug']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        sets = form.instance.group.set_set.all()
        if Group.objects.get(slug=group_slug, members=self.request.user):
            for s in sets:
                if form.instance.name == s.name:
                    raise forms.ValidationError("Set exist")
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise forms.ValidationError("Group incorrect")

    def get_success_url(self):
        return reverse_lazy('group_detail', args=[self.object.group.slug]) + '?created'


class SetDelete(DeleteView):
    model = Set

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = Set.objects.filter(group__slug=self.kwargs['slug'], slug=self.kwargs['set']).filter(
            group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': self.kwargs['slug'], 'set': self.kwargs['set']}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = Set.objects.filter(group__slug=self.kwargs['slug'], slug=self.kwargs['set'],
                                      group__members=self.request.user)
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('group_detail', args=[self.kwargs['slug']]) + '?deleted'


# Items

class MyStorageView2(PrivateStorageView):
    storage = storage2

    def can_access_file(self, private_file):
        groups = Group.objects.filter(members=self.request.user)
        group_name = self.request.path.split('/')
        group = Group.objects.get(pk=group_name[2])
        for g in groups:
            if g.pk == group.pk:
                return self.request


class KeyDetail(DetailView):
    model = Key

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Key.objects.get(slug=self.kwargs['key'], set__slug=self.kwargs['set'], set__group__slug=self.kwargs['slug'],
                           set__group__members=self.request.user):
            queryset = Key.objects.get(slug=self.kwargs['key'], set__slug=self.kwargs['set'],
                                       set__group__slug=self.kwargs['slug'], set__group__members=self.request.user)

        if not queryset:
            raise Http404

        return queryset


class KeyCreate(CreateView):
    model = Key
    form_class = KeyForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        form.instance.set = Set.objects.get(group__slug=group_slug, slug=set_slug)
        if form.instance.group == form.instance.set.group:
            for k in form.instance.set.key_set.all():
                if k.name == form.instance.name:
                    raise forms.ValidationError("Key exist")
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('set_detail', args=[self.object.group.slug, self.object.set.slug]) + '?created'


class KeyUpdate(UpdateView):
    form_class = KeyForm
    template_name_suffix = '_update_form'

    #No hay que usar form_valid en update view, hace que se ejecute dos veces el guardado de modelo y como uso cifrado lo realiza 2 veces.
    #def form_valid(self, form):
        #form.instance.last_modified_by = self.request.user
        #self.object = form.save()
        #return super().form_valid(form)

    def get_queryset(self):
        return Key.objects.filter(set__group__members=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Key.objects.get(slug=self.kwargs['key'], set__group__slug=self.kwargs['slug'], set__slug=self.kwargs['set'],
                           set__group__members=self.request.user):
            queryset = Key.objects.get(slug=self.kwargs['key'], set__group__slug=self.kwargs['slug'],
                                       set__slug=self.kwargs['set'], set__group__members=self.request.user)

        context = {'las_modified_by': self.request.user.username}

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('key_update', args=[self.object.set.group.slug, self.object.set.slug, self.object.slug]) + '?edited'


class KeyDelete(DeleteView):
    model = Key

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        key_slug = self.kwargs['key']

        queryset = Key.objects.filter(set__group__slug=group_slug, set__slug=set_slug, slug=key_slug).filter(
            set__group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': group_slug, 'set': set_slug, 'key': key_slug}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = Key.objects.filter(set__group__slug=self.kwargs['slug'], set__slug=self.kwargs['set'],
                                      slug=self.kwargs['key'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('set_detail', args=[self.kwargs['slug'], self.kwargs['set']]) + '?deleted'


class GuideDetail(DetailView):
    model = Guide

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Guide.objects.get(slug=self.kwargs['guide'], set__slug=self.kwargs['set'],
                             set__group__slug=self.kwargs['slug'], set__group__members=self.request.user):
            queryset = Guide.objects.get(slug=self.kwargs['guide'], set__slug=self.kwargs['set'],
                                         set__group__slug=self.kwargs['slug'], set__group__members=self.request.user)

        if not queryset:
            raise Http404

        return queryset


class GuideCreate(CreateView):
    model = Guide
    form_class = GuideForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        form.instance.set = Set.objects.get(group__slug=group_slug, slug=set_slug)
        if form.instance.group == form.instance.set.group:
            for k in form.instance.set.guide_set.all():
                if k.name == form.instance.name:
                    raise forms.ValidationError("Guide exist")
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('set_detail', args=[self.object.group.slug, self.object.set.slug]) + '?created'


class GuideUpdate(UpdateView):
    form_class = GuideForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return Guide.objects.filter(set__group__members=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Guide.objects.get(slug=self.kwargs['guide'], set__group__slug=self.kwargs['slug'],
                             set__slug=self.kwargs['set'], set__group__members=self.request.user):
            queryset = Guide.objects.get(slug=self.kwargs['guide'], set__group__slug=self.kwargs['slug'],
                                         set__slug=self.kwargs['set'], set__group__members=self.request.user)

        context = {'las_modified_by': self.request.user.username}

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('guide_update',
                            args=[self.object.set.group.slug, self.object.set.slug, self.object.slug]) + '?edited'


class GuideDelete(DeleteView):
    model = Guide

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        guide_slug = self.kwargs['guide']

        queryset = Guide.objects.filter(set__group__slug=group_slug, set__slug=set_slug, slug=guide_slug).filter(
            set__group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': group_slug, 'set': set_slug, 'key': guide_slug}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = Guide.objects.filter(set__group__slug=self.kwargs['slug'], set__slug=self.kwargs['set'],
                                        slug=self.kwargs['guide'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('set_detail', args=[self.kwargs['slug'], self.kwargs['set']]) + '?deleted'


class BackupDetail(DetailView):
    model = Backup

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Backup.objects.get(slug=self.kwargs['backup'], set__slug=self.kwargs['set'],
                              set__group__slug=self.kwargs['slug'], set__group__members=self.request.user):
            queryset = Backup.objects.get(slug=self.kwargs['backup'], set__slug=self.kwargs['set'],
                                          set__group__slug=self.kwargs['slug'], set__group__members=self.request.user)

        if not queryset:
            raise Http404

        return queryset


class BackupCreate(CreateView):
    model = Backup
    form_class = BackupForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        form.instance.set = Set.objects.get(group__slug=group_slug, slug=set_slug)
        if form.instance.group == form.instance.set.group:
            for k in form.instance.set.backup_set.all():
                if k.name == form.instance.name:
                    raise forms.ValidationError("Backup exist")
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('set_detail', args=[self.object.group.slug, self.object.set.slug]) + '?created'


class BackupUpdate(UpdateView):
    form_class = BackupForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return Survey.objects.filter(set__group__members=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Backup.objects.get(slug=self.kwargs['backup'], set__group__slug=self.kwargs['slug'],
                              set__slug=self.kwargs['set'], set__group__members=self.request.user):
            queryset = Backup.objects.get(slug=self.kwargs['backup'], set__group__slug=self.kwargs['slug'],
                                          set__slug=self.kwargs['set'], set__group__members=self.request.user)

        context = {'las_modified_by': self.request.user.username}

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('backup_update',
                            args=[self.object.set.group.slug, self.object.set.slug, self.object.slug]) + '?edited'


class BackupDelete(DeleteView):
    model = Backup

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        backup_slug = self.kwargs['backup']

        queryset = Backup.objects.filter(set__group__slug=group_slug, set__slug=set_slug, slug=backup_slug).filter(
            set__group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': group_slug, 'set': set_slug, 'backup': backup_slug}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = Backup.objects.filter(set__group__slug=self.kwargs['slug'], set__slug=self.kwargs['set'],
                                         slug=self.kwargs['backup'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('set_detail', args=[self.kwargs['slug'], self.kwargs['set']]) + '?deleted'


class SurveyDetail(DetailView):
    model = Survey

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Survey.objects.get(slug=self.kwargs['survey'], set__group__slug=self.kwargs['slug'],
                              set__slug=self.kwargs['set'], set__group__members=self.request.user):
            queryset = Survey.objects.get(slug=self.kwargs['survey'], set__group__slug=self.kwargs['slug'],
                                          set__slug=self.kwargs['set'], set__group__members=self.request.user)

        if not queryset:
            raise Http404

        return queryset


class SurveyCreate(CreateView):
    model = Survey
    form_class = SurveyForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        form.instance.set = Set.objects.get(group__slug=group_slug, slug=set_slug)
        if form.instance.group == form.instance.set.group:
            for k in form.instance.set.survey_set.all():
                if k.name == form.instance.name:
                    raise forms.ValidationError("Survey exist")
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('set_detail', args=[self.object.group.slug, self.object.set.slug]) + '?created'


class SurveyUpdate(UpdateView):
    form_class = SurveyForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return Survey.objects.filter(set__group__members=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if Survey.objects.get(slug=self.kwargs['survey'], set__group__slug=self.kwargs['slug'],
                              set__slug=self.kwargs['set'], set__group__members=self.request.user):
            queryset = Survey.objects.get(slug=self.kwargs['survey'], set__group__slug=self.kwargs['slug'],
                                          set__slug=self.kwargs['set'], set__group__members=self.request.user)

        context = {'las_modified_by': self.request.user.username}

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('survey_update',
                            args=[self.object.set.group.slug, self.object.set.slug, self.object.slug]) + '?edited'


class SurveyDelete(DeleteView):
    model = Survey

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']

        queryset = Survey.objects.filter(set__group__slug=group_slug, set__slug=set_slug, slug=survey_slug).filter(
            set__group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': group_slug, 'set': set_slug, 'key': survey_slug}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = Survey.objects.filter(set__group__slug=self.kwargs['slug'], set__slug=self.kwargs['set'],
                                         slug=self.kwargs['survey'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('set_detail', args=[self.kwargs['slug'], self.kwargs['set']]) + '?deleted'


class SurveyUserList(ListView):
    model = SurveyUser

    def get_queryset(self):
        return SurveyUser.objects.filter(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__set__group__members=self.request.user)


class SurveyUserCreate(CreateView):
    model = SurveyUser
    form_class = SurveyUserForm

    def form_valid(self, form):
        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        form.instance.set = Set.objects.get(group__slug=group_slug, slug=set_slug)
        form.instance.survey = Survey.objects.get(set__group__slug=group_slug, set__slug=set_slug, slug=survey_slug)
        if form.instance.group == form.instance.set.group:
            for k in form.instance.set.survey_set.all():
                if k.set == form.instance.survey.set:
                    for j in form.instance.survey.surveyuser_set.all():
                        if j.name == form.instance.name:
                            raise forms.ValidationError("Survey User exist")
                    self.object = form.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    raise forms.ValidationError("Survey not exist")
        else:
            raise forms.ValidationError("User don't have permission")

    def get_success_url(self):
        return reverse_lazy('survey_detail', args=[self.object.set.group.slug, self.object.set.slug, self.object.survey.slug]) + '?created'


class SurveyUserUpdate(UpdateView):
    form_class = SurveyUserForm
    template_name_suffix = '_update_form'

    def get_queryset(self):

        return SurveyUser.objects.filter(survey__set__group__members=self.request.user)

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        if SurveyUser.objects.get(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], slug=self.kwargs['surveyuser'], survey__set__group__members=self.request.user):
            queryset = SurveyUser.objects.get(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], slug=self.kwargs['surveyuser'], survey__set__group__members=self.request.user)

        context = {'las_modified_by': self.request.user.username}

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('surveyuser_update', args=[self.object.survey.set.group.slug, self.object.survey.set.slug, self.object.survey.slug, self.object.slug]) + '?edited'


class SurveyUserDelete(DeleteView):
    model = SurveyUser

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']
        surveyuser_slug = self.kwargs['surveyuser']

        queryset = SurveyUser.objects.filter(survey__set__group__slug=group_slug, survey__set__slug=set_slug, survey__slug=survey_slug, slug=surveyuser_slug).filter(
            survey__set__group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': group_slug, 'set': set_slug, 'survey': survey_slug, 'surveyuser': surveyuser_slug}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = SurveyUser.objects.filter(survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__slug=self.kwargs['survey'], slug=self.kwargs['surveyuser'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if SurveyUser.objects.filter(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__set__group__members=self.request.user):
          return reverse_lazy('surveyuser_list', args=[self.kwargs['slug'], self.kwargs['set'], self.kwargs['survey']]) + '?deleted'
        else:
         return reverse_lazy('survey_detail', args=[self.kwargs['slug'], self.kwargs['set'], self.kwargs['survey']]) + '?deleted'


class SurveyWorkStationList(ListView):
    model = SurveyWorkStation

    def get_queryset(self):
        return SurveyWorkStation.objects.filter(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'],
                                         survey__set__slug=self.kwargs['set'],
                                         survey__set__group__members=self.request.user)


class SurveyWorkStationCreate(CreateView):
    model = SurveyWorkStation
    form_class = SurveyWorkStationForm

    def form_valid(self, form):
        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        form.instance.set = Set.objects.get(group__slug=group_slug, slug=set_slug)
        form.instance.survey = Survey.objects.get(set__group__slug=group_slug, set__slug=set_slug, slug=survey_slug)
        if form.instance.group == form.instance.set.group:
            for k in form.instance.set.survey_set.all():
                if k.set == form.instance.survey.set:
                    for j in form.instance.survey.surveyworkstation_set.all():
                        if j.name == form.instance.name:
                            raise forms.ValidationError("Survey Workstation exist")
                    self.object = form.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    raise forms.ValidationError("Survey not exist")

        else:
            raise forms.ValidationError("User don't have permission")

    def get_success_url(self):
        return reverse_lazy('survey_detail', args=[self.object.group.slug, self.object.set.slug, self.object.survey.slug]) + '?created'


class SurveyWorkStationUpdate(UpdateView):
    form_class = SurveyWorkStationForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return SurveyWorkStation.objects.filter(survey__set__group__members=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if SurveyWorkStation.objects.get(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], slug=self.kwargs['surveyworkstation'], survey__set__group__members=self.request.user):
            queryset = SurveyWorkStation.objects.get(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], slug=self.kwargs['surveyworkstation'], survey__set__group__members=self.request.user)

        context = {'las_modified_by': self.request.user.username}

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('surveyworkstation_update', args=[self.object.survey.set.group.slug, self.object.survey.set.slug, self.object.survey.slug, self.object.slug]) + '?edited'


class SurveyWorkStationDelete(DeleteView):
    model = SurveyWorkStation

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']
        surveyworkstation_slug = self.kwargs['surveyworkstation']

        queryset = SurveyWorkStation.objects.filter(survey__set__group__slug=group_slug, survey__set__slug=set_slug, survey__slug=survey_slug, slug=surveyworkstation_slug).filter(
            survey__set__group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': group_slug, 'set': set_slug, 'survey': survey_slug, 'surveyworkstation': surveyworkstation_slug}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = SurveyWorkStation.objects.filter(survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__slug=self.kwargs['survey'], slug=self.kwargs['surveyworkstation'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if SurveyWorkStation.objects.filter(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__set__group__members=self.request.user):
          return reverse_lazy('surveyworkstation_list', args=[self.kwargs['slug'], self.kwargs['set'], self.kwargs['survey']]) + '?deleted'
        else:
         return reverse_lazy('survey_detail', args=[self.kwargs['slug'], self.kwargs['set'], self.kwargs['survey']]) + '?deleted'


class SurveyServerList(ListView):
    model = SurveyServer

    def get_queryset(self):
        return SurveyServer.objects.filter(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__set__group__members=self.request.user)


class SurveyServerCreate(CreateView):
    model = SurveyServer
    form_class = SurveyServerForm

    def form_valid(self, form):
        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        form.instance.set = Set.objects.get(group__slug=group_slug, slug=set_slug)
        form.instance.survey = Survey.objects.get(set__group__slug=group_slug, set__slug=set_slug, slug=survey_slug)
        if form.instance.group == form.instance.set.group:
            for k in form.instance.set.survey_set.all():
                if k.set == form.instance.survey.set:
                    for j in form.instance.survey.surveyserver_set.all():
                        if j.name == form.instance.name:
                            raise forms.ValidationError("Survey Server exist")
                    self.object = form.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    raise forms.ValidationError("Survey not exist")

        else:
            raise forms.ValidationError("User don't have permission")

    def get_success_url(self):
        return reverse_lazy('survey_detail', args=[self.object.group.slug, self.object.set.slug, self.object.survey.slug]) + '?created'


class SurveyServerUpdate(UpdateView):
    form_class = SurveyServerForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return SurveyServer.objects.filter(survey__set__group__members=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if SurveyServer.objects.get(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], slug=self.kwargs['surveyserver'], survey__set__group__members=self.request.user):
            queryset = SurveyServer.objects.get(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], slug=self.kwargs['surveyserver'], survey__set__group__members=self.request.user)

        context = {'las_modified_by': self.request.user.username}

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('surveyserver_update', args=[self.object.survey.set.group.slug, self.object.survey.set.slug, self.object.survey.slug, self.object.slug]) + '?edited'


class SurveyServerDelete(DeleteView):
    model = SurveyServer

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']
        surveyserver_slug = self.kwargs['surveyserver']

        queryset = SurveyServer.objects.filter(survey__set__group__slug=group_slug, survey__set__slug=set_slug, survey__slug=survey_slug, slug=surveyserver_slug).filter(
            survey__set__group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': group_slug, 'set': set_slug, 'survey': survey_slug, 'surveyserver': surveyserver_slug}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = SurveyServer.objects.filter(survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__slug=self.kwargs['survey'], slug=self.kwargs['surveyserver'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if SurveyServer.objects.filter(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__set__group__members=self.request.user):
          return reverse_lazy('surveyserver_list', args=[self.kwargs['slug'], self.kwargs['set'], self.kwargs['survey']]) + '?deleted'
        else:
         return reverse_lazy('survey_detail', args=[self.kwargs['slug'], self.kwargs['set'], self.kwargs['survey']]) + '?deleted'


class SurveyDeviceList(ListView):
    model = SurveyDevice

    def get_queryset(self):
        return SurveyDevice.objects.filter(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__set__group__members=self.request.user)


class SurveyDeviceCreate(CreateView):
    model = SurveyDevice
    form_class = SurveyDeviceForm

    def form_valid(self, form):
        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']
        form.instance.group = Group.objects.get(slug=group_slug, members=self.request.user)
        form.instance.set = Set.objects.get(group__slug=group_slug, slug=set_slug)
        form.instance.survey = Survey.objects.get(set__group__slug=group_slug, set__slug=set_slug, slug=survey_slug)
        if form.instance.group == form.instance.set.group:
            for k in form.instance.set.survey_set.all():
                if k.set == form.instance.survey.set:
                    for j in form.instance.survey.surveydevice_set.all():
                        if j.name == form.instance.name:
                            raise forms.ValidationError("Survey Device exist")
                    self.object = form.save()
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    raise forms.ValidationError("Survey not exist")

        else:
            raise forms.ValidationError("User don't have permission")

    def get_success_url(self):
        return reverse_lazy('survey_detail', args=[self.object.group.slug, self.object.set.slug, self.object.survey.slug]) + '?created'


class SurveyDeviceUpdate(UpdateView):
    form_class = SurveyDeviceForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return SurveyDevice.objects.filter(survey__set__group__members=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if SurveyDevice.objects.get(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], slug=self.kwargs['surveydevice'], survey__set__group__members=self.request.user):
            queryset = SurveyDevice.objects.get(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], slug=self.kwargs['surveydevice'], survey__set__group__members=self.request.user)

        context = {'las_modified_by': self.request.user.username}

        if not queryset:
            raise Http404

        return queryset

    def get_success_url(self):
        return reverse_lazy('surveydevice_update', args=[self.object.survey.set.group.slug, self.object.survey.set.slug, self.object.survey.slug, self.object.slug]) + '?edited'


class SurveyDeviceDelete(DeleteView):
    model = SurveyDevice

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        group_slug = self.kwargs['slug']
        set_slug = self.kwargs['set']
        survey_slug = self.kwargs['survey']
        surveydevice_slug = self.kwargs['surveydevice']

        queryset = SurveyDevice.objects.filter(survey__set__group__slug=group_slug, survey__set__slug=set_slug, survey__slug=survey_slug, slug=surveydevice_slug).filter(survey__set__group__members=self.request.user)

        if not queryset:
            raise Http404

        context = {'group': group_slug, 'set': set_slug, 'survey': survey_slug, 'surveydevice': surveydevice_slug}
        return context

    def delete(self, request, *args, **kwargs):

        queryset = SurveyDevice.objects.filter(survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__slug=self.kwargs['survey'], slug=self.kwargs['surveydevice'])
        queryset.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if SurveyDevice.objects.filter(survey__slug=self.kwargs['survey'], survey__set__group__slug=self.kwargs['slug'], survey__set__slug=self.kwargs['set'], survey__set__group__members=self.request.user):
          return reverse_lazy('surveydevice_list', args=[self.kwargs['slug'], self.kwargs['set'], self.kwargs['survey']]) + '?deleted'
        else:
         return reverse_lazy('survey_detail', args=[self.kwargs['slug'], self.kwargs['set'], self.kwargs['survey']]) + '?deleted'


# qr

def search_qr_set(request, pk):
    try:
        set = Set.objects.get(pk=pk)
        group = Group.objects.get(slug=set.group.slug)
        url = 'https://itmanager.site/set_detail/'+group.slug+'/'+set.slug
    except Set.DoesNotExist:
        raise Http404("Object does not exist")
    return HttpResponseRedirect(url)

def search_qr_key(request, pk):
    try:
        key = Key.objects.get(pk=pk)
        set = Set.objects.get(group=key.set.group, slug=key.set.slug)
        group = Group.objects.get(slug=set.group.slug)
        url = 'https://itmanager.site/key_detail/'+group.slug+'/'+set.slug+'/'+key.slug
    except Set.DoesNotExist:
        raise Http404("Object does not exist")
    return HttpResponseRedirect(url)

def search_qr_backup(request, pk):
    try:
        backup = Backup.objects.get(pk=pk)
        set = Set.objects.get(group=backup.set.group, slug=backup.set.slug)
        group = Group.objects.get(slug=set.group.slug)
        url = 'https://itmanager.site/backup_detail/'+group.slug+'/'+set.slug+'/'+backup.slug
    except Set.DoesNotExist:
        raise Http404("Object does not exist")
    return HttpResponseRedirect(url)

def search_qr_guide(request, pk):
    try:
        guide = Guide.objects.get(pk=pk)
        set = Set.objects.get(group=guide.set.group, slug=guide.set.slug)
        group = Group.objects.get(slug=set.group.slug)
        url = 'https://itmanager.site/guide_detail/'+group.slug+'/'+set.slug+'/'+guide.slug
    except Set.DoesNotExist:
        raise Http404("Object does not exist")
    return HttpResponseRedirect(url)

def search_qr_survey(request, pk):
    try:
        survey = Survey.objects.get(pk=pk)
        set = Set.objects.get(group=survey.set.group, slug=survey.set.slug)
        group = Group.objects.get(slug=set.group.slug)
        url = 'https://itmanager.site/survey_detail/'+group.slug+'/'+set.slug+'/'+survey.slug
    except Set.DoesNotExist:
        raise Http404("Object does not exist")
    return HttpResponseRedirect(url)

