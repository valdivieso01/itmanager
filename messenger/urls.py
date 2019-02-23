from django.urls import path
from .views import ThreadList, ThreadDetail, add_message, start_thread
from django.contrib.auth.decorators import login_required

messenger_patterns = ([
    path('', login_required(ThreadList.as_view()), name="list"),
    path('thread/<int:pk>/', login_required(ThreadDetail.as_view()), name="detail"),
    path('thread/<int:pk>/add/', login_required(add_message), name="add"),
    path('thread/start/<username>/', login_required(start_thread), name="start")
], "messenger")