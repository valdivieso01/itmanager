from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache
from registration.views import MyStorageView1
from .views import HomePage, KeyCreate, KeyDetail, \
    KeyDelete, KeyUpdate, BackupCreate, BackupDetail, BackupDelete, BackupUpdate, GroupList, GroupDetail, \
    GroupCreate, GroupDelete, GroupUpdate, SetCreate, SetUpdate, SetDetail, SetDelete, GuideCreate, GuideDetail, \
    GuideDelete, GuideUpdate, SurveyCreate, SurveyDetail, SurveyDelete, SurveyUpdate, SurveyUserCreate, \
    SurveyUserDelete, SurveyUserUpdate, SurveyUserList, SurveyWorkStationDelete, SurveyWorkStationUpdate, \
    SurveyWorkStationCreate, SurveyWorkStationList, SurveyServerCreate, SurveyServerList, SurveyServerDelete, \
    SurveyServerUpdate, SurveyDeviceCreate, SurveyDeviceList, SurveyDeviceDelete, SurveyDeviceUpdate, MyStorageView2, search_qr_set, search_qr_key, search_qr_backup, search_qr_guide, search_qr_survey

urlpatterns = [
    # path private files
    url('^user-private/(?P<path>.*)$', MyStorageView1.as_view()),
    url('^group-private/(?P<path>.*)$', MyStorageView2.as_view()),
    url(r'^ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),
    # path home
    path('', login_required(HomePage.as_view()), name="home"),
    # paths groups
    path('group_list', login_required(GroupList.as_view()), name="group_list"),
    path('group_create', login_required(GroupCreate.as_view()), name="group_create"),
    path('group_delete/<slug:slug>', login_required(GroupDelete.as_view()), name="group_delete"),
    path('group_detail/<slug:slug>', login_required(GroupDetail.as_view()), name="group_detail"),
    path('group_update/<slug:slug>', login_required(GroupUpdate.as_view()), name="group_update"),
    # paths sets
    path('set_create/<slug:slug>', login_required(SetCreate.as_view()), name="set_create"),
    path('set_detail/<slug:slug>/<slug:set>', login_required(SetDetail.as_view()), name="set_detail"),
    path('set_update/<slug:slug>/<slug:set>', login_required(SetUpdate.as_view()), name="set_update"),
    path('set_delete/<slug:slug>/<slug:set>', login_required(SetDelete.as_view()), name="set_delete"),
    # paths items
    path('key_create/<slug:slug>/<slug:set>', login_required(KeyCreate.as_view()), name="key_create"),
    path('key_detail/<slug:slug>/<slug:set>/<slug:key>', login_required(KeyDetail.as_view()), name="key_detail"),
    path('key_delete/<slug:slug>/<slug:set>/<slug:key>', login_required(KeyDelete.as_view()), name="key_delete"),
    path('key_update/<slug:slug>/<slug:set>/<slug:key>', login_required(KeyUpdate.as_view()), name="key_update"),
    path('guide_create/<slug:slug>/<slug:set>', login_required(GuideCreate.as_view()), name="guide_create"),
    path('guide_detail/<slug:slug>/<slug:set>/<slug:guide>', login_required(GuideDetail.as_view()), name="guide_detail"),
    path('guide_delete/<slug:slug>/<slug:set>/<slug:guide>', login_required(GuideDelete.as_view()), name="guide_delete"),
    path('guide_update/<slug:slug>/<slug:set>/<slug:guide>', login_required(GuideUpdate.as_view()), name="guide_update"),
    path('backup_create/<slug:slug>/<slug:set>', login_required(BackupCreate.as_view()), name="backup_create"),
    path('backup_detail/<slug:slug>/<slug:set>/<slug:backup>', login_required(BackupDetail.as_view()), name="backup_detail"),
    path('backup_delete/<slug:slug>/<slug:set>/<slug:backup>', login_required(BackupDelete.as_view()), name="backup_delete"),
    path('backup_update/<slug:slug>/<slug:set>/<slug:backup>', login_required(BackupUpdate.as_view()), name="backup_update"),
    path('survey_create/<slug:slug>/<slug:set>', login_required(SurveyCreate.as_view()), name="survey_create"),
    path('survey_detail/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyDetail.as_view()), name="survey_detail"),
    path('survey_delete/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyDelete.as_view()), name="survey_delete"),
    path('survey_update/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyUpdate.as_view()), name="survey_update"),
    path('surveyuser_create/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyUserCreate.as_view()), name="surveyuser_create"),
    path('surveyuser_list/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyUserList.as_view()), name="surveyuser_list"),
    path('surveyuser_delete/<slug:slug>/<slug:set>/<slug:survey>/<slug:surveyuser>', login_required(SurveyUserDelete.as_view()), name="surveyuser_delete"),
    path('surveyuser_update/<slug:slug>/<slug:set>/<slug:survey>/<slug:surveyuser>', login_required(SurveyUserUpdate.as_view()), name="surveyuser_update"),
    path('surveyworkstation_create/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyWorkStationCreate.as_view()), name="surveyworkstation_create"),
    path('surveyworkstation_list/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyWorkStationList.as_view()), name="surveyworkstation_list"),
    path('surveyworkstation_delete/<slug:slug>/<slug:set>/<slug:survey>/<slug:surveyworkstation>', login_required(SurveyWorkStationDelete.as_view()), name="surveyworkstation_delete"),
    path('surveyworkstation_update/<slug:slug>/<slug:set>/<slug:survey>/<slug:surveyworkstation>', login_required(SurveyWorkStationUpdate.as_view()), name="surveyworkstation_update"),
    path('surveyserver_create/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyServerCreate.as_view()), name="surveyserver_create"),
    path('surveyserver_list/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyServerList.as_view()), name="surveyserver_list"),
    path('surveyserver_delete/<slug:slug>/<slug:set>/<slug:survey>/<slug:surveyserver>', login_required(SurveyServerDelete.as_view()), name="surveyserver_delete"),
    path('surveyserver_update/<slug:slug>/<slug:set>/<slug:survey>/<slug:surveyserver>', login_required(SurveyServerUpdate.as_view()), name="surveyserver_update"),
    path('surveydevice_create/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyDeviceCreate.as_view()), name="surveydevice_create"),
    path('surveydevice_list/<slug:slug>/<slug:set>/<slug:survey>', login_required(SurveyDeviceList.as_view()), name="surveydevice_list"),
    path('surveydevice_delete/<slug:slug>/<slug:set>/<slug:survey>/<slug:surveydevice>', login_required(SurveyDeviceDelete.as_view()), name="surveydevice_delete"),
    path('surveydevice_update/<slug:slug>/<slug:set>/<slug:survey>/<slug:surveydevice>', login_required(SurveyDeviceUpdate.as_view()), name="surveydevice_update"),
    #paths qr
    path('search_qr_set/<int:pk>', search_qr_set, name="search_qr_set"),
    path('search_qr_key/<int:pk>', search_qr_key, name="search_qr_key"),
    path('search_qr_backup/<int:pk>', search_qr_backup, name="search_qr_backup"),
    path('search_qr_guide/<int:pk>', search_qr_guide, name="search_qr_guide"),
    path('search_qr_survey/<int:pk>', search_qr_survey, name="search_qr_survey"),
]
