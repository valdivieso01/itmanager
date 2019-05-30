from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import ProfileUpdate, EmailUpdate, KeyCreate, KeyDetail, KeyDelete, KeyUpdate, NoteCreate, NoteDetail, NoteDelete, NoteUpdate, NoteList, KeyList, GuideDetail, GuideDelete, GuideUpdate, GuideList, GuideCreate, UserDelete, UserList, UserCreate, Login

urlpatterns = [

    path('', Login.as_view(), name="login"),
    path('create/', login_required(UserCreate.as_view()), name="user_create"),
    path('delete/<username>/', login_required(UserDelete.as_view()), name="user_delete"),
    path('list/', login_required(UserList.as_view()), name="user_list"),
    path('profile/', login_required(ProfileUpdate.as_view()), name="profile"),
    path('profile/email/', login_required(EmailUpdate.as_view()), name="profile_email"),
    path('key_list/', login_required(KeyList.as_view()), name="key_list"),
    path('key_create/', login_required(KeyCreate.as_view()), name="key_create"),
    path('key_detail/<slug:slug>/', login_required(KeyDetail.as_view()), name="key_detail"),
    path('key_delete/<slug:slug>/', login_required(KeyDelete.as_view()), name="key_delete"),
    path('key_update/<slug:slug>/', login_required(KeyUpdate.as_view()), name="key_update"),
    path('note_list/', login_required(NoteList.as_view()), name="note_list"),
    path('note_create/', login_required(NoteCreate.as_view()), name="note_create"),
    path('note_detail/<slug:slug>/', login_required(NoteDetail.as_view()), name="note_detail"),
    path('note_delete/<slug:slug>/', login_required(NoteDelete.as_view()), name="note_delete"),
    path('note_update/<slug:slug>/', login_required(NoteUpdate.as_view()), name="note_update"),
    path('guide_list/', login_required(GuideList.as_view()), name="guide_list"),
    path('guide_create/', login_required(GuideCreate.as_view()), name="guide_create"),
    path('guide_detail/<slug:slug>/', login_required(GuideDetail.as_view()), name="guide_detail"),
    path('guide_delete/<slug:slug>/', login_required(GuideDelete.as_view()), name="guide_delete"),
    path('guide_update/<slug:slug>/', login_required(GuideUpdate.as_view()), name="guide_update"),
]
